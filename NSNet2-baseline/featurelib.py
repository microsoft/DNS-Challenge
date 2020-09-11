import numpy as np
import soundfile as sf
from pathlib import Path
from scipy.signal import blackman, blackmanharris


def calcFeat(Spec, cfg):
    """compute spectral features"""

    if cfg['feattype'] == "MagSpec":
        inpFeat = np.abs(Spec)

    elif cfg['feattype'] == "LogPow":
        pmin = 10**(-12)
        powSpec = np.abs(Spec)**2
        inpFeat = np.log10(np.maximum(powSpec, pmin))

    else:
        ValueError('Feature not implemented.')
    
    return inpFeat


def calcSpec(y, params, channel=None):
    """compute complex spectrum from audio file"""

    fs = int(params["fs"])

    if channel is not None and (len(y.shape)>1):
        # use only single channel
        sig = sig[:,channel]

    # STFT parameters
    N_win = int(float(params["winlen"])*fs)
    if 'nfft' in params:
        N_fft = int(params['nfft'])
    else:
        N_fft = int(float(params['winlen'])*fs)
    N_hop = int(N_win * float(params["hopfrac"]))
    win = np.sqrt(np.hanning(N_win))

    Y = stft(y, N_fft, win, N_hop)

    return Y


def spec2sig(Spec, params):
    """convert spectrum to time signal"""

    # STFT parameters
    fs = int(params["fs"])
    N_win = int(float(params["winlen"])*fs)
    if 'nfft' in params:
        N_fft = int(params['nfft'])
    else:
        N_fft = int(float(params['winlen'])*fs)
    N_hop = int(N_win * float(params["hopfrac"]))
    win = np.sqrt(np.hanning(N_win))

    x = istft(Spec, N_fft, win, N_hop)

    return x


# STFT
def stft(x, N_fft, win, N_hop, nodelay=True):
	"""
	short-time Fourier transform
		x 			time domain signal [samples x channels]
		N_fft 		FFT size (samples)
		win 		window,  len(win) <= N_fft
		N_hop 		hop size (samples)
		nodelay 	[True,False]: do not introduce delay (visible windowing effects in first frames)
	"""
	# get lengths
	if x.ndim == 1:
		x = x[:,np.newaxis]
	Nx = x.shape[0]
	M = x.shape[1]
	specsize = int(N_fft/2+1)
	N_win = len(win)
	N_frames = int(np.ceil( (Nx+N_win-N_hop)/N_hop ))
	Nx = N_frames*N_hop # padded length
	x = np.vstack([x, np.zeros((Nx-len(x),M))])
	
	# init
	X_spec = np.zeros((specsize,N_frames,M), dtype=complex)
	win_M = np.outer(win,np.ones((1,M)))
	x_frame = np.zeros((N_win,M))
	for nn in range(0,N_frames):
		idx = int(nn*N_hop)
		x_frame = np.vstack((x_frame[N_hop:,:], x[idx:idx+N_hop,:]))
		x_win = win_M * x_frame
		X = np.fft.rfft(x_win, N_fft, axis=0)
		X_spec[:,nn,:] = X

	if nodelay:
		delay = int(N_win/N_hop - 1)
		X_spec = X_spec[:,delay:,:]

	if M==1:
		X_spec = np.squeeze(X_spec)
	
	return X_spec


def istft(X, N_fft, win, N_hop):
	"""
	inverse short-time Fourier transform
		X 			Spectra [frequency x frames x channels]
		N_fft 		FFT size (samples)
		win 		window,  len(win) <= N_fft
		N_hop 		hop size (samples)
	"""
	# get lengths
	specsize = X.shape[0]
	N_frames = X.shape[1]
	if X.ndim < 3:
		X = X[:,:,np.newaxis]
	M = X.shape[2]
	N_win = len(win)
	
	# init
	Nx = N_hop*(N_frames-1) + N_win
	win_M = np.outer(win,np.ones((1,M)))
	x = np.zeros((Nx,M))
	
	for nn in range(0,N_frames):
		X_frame = np.squeeze(X[:,nn,:])
		x_win = np.fft.irfft(X_frame, N_fft, axis=0)
		x_win = x_win.reshape(N_fft,M)
		x_win = win_M * x_win[0:N_win,:]
		idx1 = int(nn*N_hop); idx2 = int(idx1+N_win)
		x[idx1:idx2,:] = x_win + x[idx1:idx2,:]
	
	if M==1:
		x = np.squeeze(x)
	
	return x


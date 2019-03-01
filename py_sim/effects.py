import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

import audio


def triangular(xn: list, exp: float = 3, gain: float = 1) -> list:
  yn = np.ndarray(len(xn)).astype(np.float32)

  for i in range(len(xn)):
    yn[i] = gain * (xn[i] + (xn[i]**exp)/3.0)

  return yn


def soft_clip(xn: list, k: float, gain: float = 1) -> list:
  yn = np.ndarray(len(xn)).astype(np.float32)

  for i in range(len(xn)):
    x = xn[i] / (10)
    yn[i] = gain * (x / (1.0 + k*np.abs(x)))
    yn[i] *= (10)
    #yn[i] = gain * (xn[i] / (100.0 + k*np.abs(xn[i])))
    #yn[i] = gain * ((xn[i]**2) - (xn[i]**3) / 3)

  return yn


def hard_clip(xn: list, threshold: float, gain: float = 1) -> list:
  yn = np.ndarray(len(xn)).astype(np.float32)

  for i in range(len(xn)):
    x = gain*xn[i]

    if x > threshold:
      yn[i] = threshold
    elif x < -1*threshold:
      yn[i] = -1*threshold
    else:
      yn[i] = x

  return yn


def asym_clip(xn: list, high: float, low: float, gain: float = 1) -> list:
  yn = np.ndarray(len(xn)).astype(np.float32)

  for i in range(len(xn)):
    x = gain*xn[i]


    if x > high:
      yn[i] = high
    elif x < low:
      yn[i] = low
    else:
      yn[i] = x

  return yn


def tremolo(xn: list) -> list:
  yn = np.ndarray(len(xn)).astype(np.float32)

  # generate triangle wave
  tn = np.ndarray(len(xn)).astype(np.float32)

  inc = 10.0/(1*len(xn))
  print(inc)

  sign = 1
  curr = 0

  for i in range(len(tn)):
    if curr >= 1.0:
      print('dir down', curr, i)
      sign = -1
    elif curr <= 0:
      print('dir up', curr, i)
      sign = 1

    tn[i] = curr

    curr = curr + (sign * inc)

  print(tn)
  yn = tn
  return tn*xn


def wah(xn: list) -> list:
  #yn = np.ndarray(len(xn)).astype(np.float32)
  l  = 30
  fc = 0.000001
  fo = 0.15
  n  = np.arange(-l, l+1, dtype=np.int)

  bk = 8300 * 2*fc*np.sinc(2*n*fc) #*sig.hamming(len(n))
  ak = [1, *[0]*len(bk-1)]

  cnt = 0

  for i in range(len(bk)):
    if np.abs(bk[i]) < 1e-4:
      bk[i] = 0
    else:
      cnt += 1

  bk_mod = bk #* 2*np.cos(2*np.pi*fo*(n+l))

  print(ak)
  print(bk)
  print(bk_mod)
  print('non zero coefficient count: {}'.format(cnt))

  (w, h) = sig.freqz(bk_mod, ak)
  plt.plot(44.1e3*w/(2*np.pi), np.abs(h))
  plt.show()
  plt.plot(bk_mod)
  plt.show()

  cw = audio.sinusoid(1, 10000, 0, 44.1e3, 1)

  return sig.lfilter(bk, ak, xn)

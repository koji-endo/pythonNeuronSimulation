: test hodgkin huxley model

NEURON {
  SUFFIX hhmodel
  USEION k READ ek WRITE ik
  USEION na READ ena WRITE ina
  NONSPECIFIC_CURRENT il
  RANGE gk, vk, gna, vna, gl, vl, gnabar, gkbar, el
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S)  = (siemens)
    (molar) = (1/liter)
    (mM)	= (millimolar)
    (nM)        = (nanomolar)
    FARADAY = (faraday) (coulomb)  :units are really coulombs/mole
    PI	= (pi) (1)
}

ASSIGNED{
 v (mV)
 ena (mV)
 ek (mV)
 il (mA/cm2)
 ik (mA/cm2)
 ina (mA/cm2)
 gna (mS/cm2)
 gk (mS/cm2)

}

PARAMETER {
  gkbar = 36.0 (mS/cm2)
  gnabar = 120 (mS/cm2)
  gl = 0.3 (mS/cm2)
  el = -65 (mV)
}

STATE {
  m n h
}

BREAKPOINT {
  SOLVE states METHOD cnexp
  gna = gnabar * pow(m, 3) * h
  ina = gna * (v - ena)
  gk = gkbar * pow(n, 4)
  ik = gk * (v - ek)
  il = gl * (v - el)

}

INITIAL {
  m = 0
  n = 0
  h = 0
}

DERIVATIVE states {
  m' = alpham(v) * (1 - m) - betam(v) * m
  h' = alphah(v) * (1 - h) - betah(v) * h
  n' = alphan(v) * (1 - n) - betan(v) * n
}

FUNCTION alpham(v (mV)) {
  alpham = 0.1 * (-40 - v)/(exp((-40-v)/10) - 1)
}
FUNCTION betam(v (mV)) {
  betam = 4 * exp((-65-v)/18)
}
FUNCTION alphah(v (mV)) {
  alphah = 0.07 * exp((-65-v)/20)
}
FUNCTION betah(v (mV)) {
  betah =  1/(exp((-35-v)/10)+1)
}
FUNCTION alphan(v (mV)) {
  alphan = 0.01 * (-55 - v)/(exp((-55-v)/10) - 1)
}
FUNCTION betan(v (mV)) {
  betan = 0.125 * exp((-65-v)/80)
}

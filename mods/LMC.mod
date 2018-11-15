: Lamina neuron model by Rusanen et al 2015
: conductance based model

NEURON {
  SUFFIX LMC
  USEION k READ ek WRITE ik
  NONSPECIFIC_CURRENT il
  RANGE gkdrbar, gkshbar, gl, gk, el
  RANGE v1, v2, v3, v4, phi
}

UNITS {
    (mA) = (milliamp)
    (uA) = (microamp)
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
 il (mA/cm2)
 ik (mA/cm2)
 gk (mS/cm2)
}

PARAMETER {
  gkshbar = 3500 (mS/cm2)
  gkdrbar = 0.151 (mS/cm2)
  gl = 97 (mS/cm2)
  el = -22.8 (mV)
  ek = -67.2 (mV)
}

BREAKPOINT {
  gk = gkshbar * m(v) * h(v)  + gkdrbar * n(v) * l(v)
  ik = gk * (v - ek)
  il = gl * (v - el)

}

FUNCTION m(v (mV)){
  m = 1/(1 + exp((v - (-60 +48.3))/-2.8))
}
FUNCTION h(v (mV)){
  h = 1/(1 + exp((v - (-101 +48.3))/-5.6))
}
FUNCTION n(v (mV)){
  n = 1/(1 + exp((v - (-60 +16.8))/-5.5))
}
FUNCTION l(v (mV)){
  l = 1/(1 + exp((v - (-84 +16.8))/-8.7))
}

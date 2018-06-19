: Lamina neuron model resembling Morris-Lecar neuron model by Lazar et al 2014
: conductance based model

NEURON {
  SUFFIX mole
  USEION k READ ek WRITE ik
  USEION ca READ eca WRITE ica
  NONSPECIFIC_CURRENT il
  NONSPECIFIC_CURRENT b
  RANGE gk, gca, gl, gkbar, gcabar, el
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
 ek (mV)
 eca (mV)
 il (mA/cm2)
 ik (mA/cm2)
 gk (mS/cm2)
 ica (mA/cm2)
 gca (mS/cm2)
}

PARAMETER {
  gkbar = 1.1 (mS/cm2)
  gcabar = 2.0 (mS/cm2)
  gl = 0.5 (mS/cm2)
  el = -50 (mV)
  v1 = -1 (mV)
  v2 = 15 (mV)
  v3 = -50 (mV)
  v4 = 1 (mV)
  b  = -0.02 (uA/cm2)
  phi = 0.0025
}

STATE {
  n
}

BREAKPOINT {
  SOLVE states METHOD cnexp
  gk = gkbar * n
  gca = 0.5 * gcabar * (1 + tanh((v - v1)/v2))
  ik = gk * (v - ek)
  ica = gca * (v - eca)
  il = gl * (v - el)

}

INITIAL {
  n = 0.5
}

DERIVATIVE states {
  n' = (0.5 * (1 + tanh((v - v3)/v4)) - n) * phi * cosh((v - v3)/(2 * v4))
}

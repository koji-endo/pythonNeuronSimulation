: Medulla inter neuron model
: conductance based model

NEURON {
  SUFFIX MIN
  USEION k READ ek WRITE ik
  USEION na READ ena WRITE ina
  NONSPECIFIC_CURRENT il
  RANGE gk, gna, gnovbar, gshbar, gdrbar, gkleak, gnabar, el, gl
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
 ek (mV)
 ena (mV)
 il (mA/cm2)
 ik (mA/cm2)
 gk (mS/cm2)
 ina (mA/cm2)
 gna (mS/cm2)
}

PARAMETER {
  gnovbar = 3.0 (mS/cm2)
  gshbar = 1.6 (mS/cm2)
  gdrbar = 3.5 (mS/cm2)
  gkleak = 0.082 (mS/cm2)
  gl = 0.006 (mS/cm2)
  gnabar = 120 (mS/cm2)
  el = -30 (mV)
}

STATE {
  m n y2 y3 y4 y5 y6
}

BREAKPOINT {
  SOLVE states METHOD cnexp
  gk = gkleak + gshbar * pow(y2, 3) * y3 + gdrbar * pow(y4, 2) * y5 + gnovbar * y6
  ik = gk * (v - ek)
  gna = gnabar * pow(m, 3) * h
  ina = gna * (v - ena)
  il = gl * (v - el)

}

INITIAL {
  y2 = 0.5
  y3 = 0.5
  y4 = 0.5
  y5 = 0.5
  y6 = 0.5
  m = 0.5
  h = 0.5
}

DERIVATIVE states {
  y2' = (y2inf(v) - y2) / y2tau(v)
  y3' = (y3inf(v) - y3) / y3tau(v)
  y4' = (y4inf(v) - y4) / y4tau(v)
  y5' = (y5inf(v) - y5) / y5tau(v)
  y6' = (y6inf(v) - y6) / y6tau(v)
  m' = alpham(v) * (1 - m) - betam(v) * m
  h' = alphah(v) * (1 - h) - betah(v) * h

}

FUNCTION y2inf(v (mV)) {
  y2inf = pow(1/(1+exp((-23.7-v)/12.8)), 1.0/3)
}
FUNCTION y2tau(v (mV)) {
  y2tau = 0.13 + 3.39 * exp(-pow((-73-v)/20.0 ,2))
}
FUNCTION y3inf(v (mV)) {
  y3inf = 0.9 / (1 + exp((-55-v)/(-3.9))) + 0.1 / (1 + exp((-74.8 - v)/(-10.7)))
}
FUNCTION y3tau(v (mV)) {
  y3tau = 113 * exp(-pow((-71-v)/29.0 ,2))
}
FUNCTION y4inf(v (mV)) {
  y4inf = sqrt(1.0/(1+exp((-1-v)/9.1)))
}
FUNCTION y4tau(v (mV)) {
  y4tau = 0.5 + 5.75 * exp(-pow((-25-v)/32.0 ,2))
}
FUNCTION y5inf(v (mV)) {
  y5inf = 1/(1+exp((-25.7-v)/(-6.4)))
}
FUNCTION y5tau(v (mV)) {
  y5tau = 890
}
FUNCTION y6inf(v (mV)) {
  y6inf = 1.0/(1+exp((-12-v)/11))
}
FUNCTION y6tau(v (mV)) {
  y6tau = 3 + 166 * exp(-pow((-20-v)/22 ,2))
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

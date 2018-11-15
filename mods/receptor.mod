: photo insensitive cell membrane model by Niven 2003
: conductance based model

NEURON {
  SUFFIX receptor
  USEION k READ ek WRITE ik
  NONSPECIFIC_CURRENT iCl
  NONSPECIFIC_CURRENT il
  RANGE gk, gl, gkleak, gnovbar, gdrbar, gshbar, gclleak, eCl, el
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
 il (mA/cm2)
 ik (mA/cm2)
 iCl (mA/cm2)
 gk (mS/cm2)
}

PARAMETER {
  gshbar = 1.6 (mS/cm2)
  gdrbar = 3.5 (mS/cm2)
  gkleak = 0.082 (mS/cm2)
  gclleak = 0.056 (mS/cm2)
  gl = 0.093 (mS/cm2)
  ek = -85 (mV)
  el = 10 (mV)
  eCl = -30 (mV)
}

STATE {
  y1 y2 y3 y4
}

BREAKPOINT {
  SOLVE states METHOD cnexp
  gk = gkleak + gshbar * pow(y1, 3) * y2 + gdrbar * pow(y3, 2) * y4
  ik = gk * (v - ek)
  iCl = gclleak * (v - eCl)
  il = gl * (v - el)

}

INITIAL {
  y1 = 0.5
  y2 = 0.5
  y3 = 0.5
  y4 = 0.5
}

DERIVATIVE states {
  y1' = alphay1(v) * (1-y1) - betay1(v) * y1
  y2' = alphay2(v) * (1-y2) - betay2(v) * y2
  y3' = alphay3(v) * (1-y3) - betay3(v) * y3
  y4' = alphay4(v) * (1-y4) - betay4(v) * y4
}

FUNCTION alphay2(v (mV)) {
  alphay2 = pow(1/(1+exp(0.117*(v+31.35))), 1/3) / y2tau(v)
}
FUNCTION betay2(v (mV)) {
  betay2 = (1 - pow(1/(1+exp(0.117*(v+31.35))), 1/3)) /y2tau(v)
}
FUNCTION alphay1(v (mV)) {
  alphay1 = (1 / (1+exp(-0.153*(v+6)))) / y1tau(v)
}
FUNCTION betay1(v (mV)) {
  betay1 = (1- (1 / (1+exp(-0.153*(v+6))))) / y1tau(v)
}
FUNCTION alphay4(v (mV)) {
  alphay4 = pow(1/(1+exp(0.153*(v+59.94))), 1/2) / y4tau(v)
}
FUNCTION betay4(v (mV)) {
  betay4 = (1 - pow(1/(1+exp(0.153*(v+59.94))), 1/2)) / y4tau(v)
}
FUNCTION alphay3(v (mV)) {
  alphay3 = (1 / (1+exp(-0.098*(v+32.52)))) / y3tau(v)
}
FUNCTION betay3(v (mV)) {
  betay3 = (1 - (1 / (1+exp(-0.098*(v+32.52))))) / y3tau(v)
}
FUNCTION y1tau(v (mV)) {
  y1tau = 3.5/(1+pow( abso((v + 80.01)/18.34), 2* 0.998 ))
}
FUNCTION y2tau(v (mV)) {
  y2tau = 115/(1+pow(abso((v + 74.46)/26.44), 2* 1.60 ))
}
FUNCTION y3tau(v (mV)) {
  y3tau = 6.4/(1+pow(abso((v + 19.13)/26.01), 2* 0.817 ))
}
FUNCTION y4tau(v (mV)) {
  y4tau = 890
}
FUNCTION abso(x) {
 if(x>= 0){
  abso = x
 }
 else {
  abso = -x
 }
}

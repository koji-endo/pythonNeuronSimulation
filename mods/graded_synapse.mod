:ribbon synapse
:graded synaptic transmission based on presynaptic voltage

NEURON {
  POINT_PROCESS gsyn
  POINTER vpost
  RANGE vth, vre, k, gsat, n, g
  NONSPECIFIC_CURRENT i
}

UNITS {
    (mA) = (milliamp)
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (S)  = (siemens)
    (uS) = (microsiemens)
    (molar) = (1/liter)
    (mM)	= (millimolar)
    (nM)        = (nanomolar)
    FARADAY = (faraday) (coulomb)  :units are really coulombs/mole
    PI	= (pi) (1)
}

PARAMETER {
  vth = -52.14(mV)
  k = 20(uS/mM3)
  gsat = 800(uS)
  n = 1
  vre = -80(mV)
}

ASSIGNED{
  v (mV)
  g (uS)
  i (nA)
  vpost (mV) : postsynaptic voltage
}

BREAKPOINT {
  if (v >= vth){
    g = k * pow((v - vth), n)
    if (g > gsat){
      g = gsat
    }
  }
  else {
    g = 0
  }
  i = g * (vpost - vre)
}

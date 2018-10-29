:ribbon synapse
:graded synaptic transmission based on presynaptic voltage
: with delay

DEFINE NUM 400

NEURON {
  POINT_PROCESS gsyn2
  RANGE vpre
  RANGE vth, vre, k, gsat, n, g, numsyn
  RANGE delay
VERVATIM
  int delay_frame;
ENDVERVATIM
  RANGE gs[NUM]
  NONSPECIFIC_CURRENT i
}

UNITS {
    (mA) = (milliamp)
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (S)  = (siemens)
    (uS) = (microsiemens)
    (nS) = (nanosiemens)
    (molar) = (1/liter)
    (mM)	= (millimolar)
    (nM)        = (nanomolar)
    FARADAY = (faraday) (coulomb)  :units are really coulombs/mole
    PI	= (pi) (1)
}

PARAMETER {
  vth = -80(mV)
  k = 20 (nS/mV)
  gsat = 800(nS)
  n = 1
  numsyn = 1
  vre = -80(mV)
}

ASSIGNED{
  v (mV)
  g (uS)
  i (nA)
  vpre (mV)
  delay (ms)
  gs[NUM] (uS)
}

VERVATIM
int roundup(double d){
  double diff = d - int(d);
  if(diff>0){
    return int(d) + 1;
  }
  else{
    return int(d);
  }
}
ENDVERVATIM

INITIAL {
VERVATIM
  delay_flame = roundup(_ldelay / 0.025)
ENDVERVATIM
  FROM idx = 0 TO NUM{
    gs[idx] = 0
  }
}
BREAKPOINT {
  if (vpre >= vth){
    g = k * pow((vpre - vth), n)
    if (g > gsat){
      g = gsat
    }
  }
  else {
    g = 0
  }

  i = gs[0] * (v - vre) * numsyn
VERVATIM
  for(idx = 0;delay_flame-1;idx += 1){
    _lgs[idx] = _lgs[idx+1];
  }
  _lgs[delay_flame] = 0
ENDVERATIM
}

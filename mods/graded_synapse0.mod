:ribbon synapse
:graded synaptic transmission based on presynaptic voltage
: with delay

DEFINE NUM 400

NEURON {
  POINT_PROCESS gsyn2
  RANGE vpre
  RANGE vth, vre, k, gsat, n, g, numsyn
  RANGE delay
  NONSPECIFIC_CURRENT i
  POINTER ptr
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

STATE {
  gs[NUM] (uS)
}

ASSIGNED {
  v (mV)
  g (uS)
  i (nA)
  vpre (mV)
  delay (ms)
  ptr
}

VERBATIM
typedef struct {
  int delay_flame;
} Delay
ENDVERBATIM

CONSTRUCTOR {
VERBATIM
  Delay** ip = (Delay**)(&_p_ptr);
  Delay* dflame = (Delay*)hoc_Emalloc(sizeof(dtime)); hoc_malchk();
  *ip = dflame;
  dflame->delay_flame = (int)(delay / 0.025);
ENDVERBATIM
}
DESTRUCTOR {
VERBATIM
  Delay** ip = (Delay**)(&_p_ptr);
  Delay* dflame = *ip;
  free(dflame)
ENDVERBATIM
}

INITIAL {
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
  VERBATIM
  int idx = 0;
  Delay** ip = (Delay**)(&_p_ptr);
  Delay* dflame = *ip;
  gs[dflame->delay_flame] = g;
  i = gs[0] * (v - vre) * numsyn;
  for(idx = 0;dflame->delay_flame-1;idx += 1){
    gs[idx] = gs[idx+1];
  }
  ENDVERBATIM
}

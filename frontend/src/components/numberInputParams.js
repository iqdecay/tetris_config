// This is used to build the number input fields
// Each item of the array is built this way :
// [key, min value, max value, step value, units (unused), label]
const numberInputParams = [
    ["seuilMinAna30v", 0, 30, .25, "V", "Seuil min tension analogique 30V"],
    ["activMinAna30v", 0, 1, 1, "", "Activation seuil min tension analogique 30V"],
    ["seuilMaxAna30v", 0, 30, .25, "V", "Seuil max tension analogique 30V"],
    ["activMaxAna30v", 0, 1, 1, "", "Activation seuil max tension analogique 30V"],
    ["seuilMinAna100mv", -100, 100, 1, "mV", "Seuil min tension analogique 100mV"],
    ["seuilMaxAna100mv", -100, 100, 1, "mV", "Seuil max tension analogique 100mV"],
    ["dureeCycleFeux", 1, 32, 1, "s", "Durée de cycles de feux"],
    ["acqPositionBase", 0, 1, 1, "", "Acquisition position"],
    ["activMinAna100mv", 0, 1, 1, "", "Activation seuil min tension analogique 100mV"],
    ["activMaxAna100mv", 0, 1, 1, "", "Activation seuil max tension analogique 100mV"],
    ["activeTor1", 0, 1, 1, "", "Alarme inactive/active TOR 1"],
    ["activeTor2", 0, 1, 1, "", "Alarme inactive/active TOR 2"],
    ["activeTor3", 0, 1, 1, "", "Alarme inactive/active TOR 3"],
    ["activeTor4", 0, 1, 1, "", "Alarme inactive/active TOR 4"],
    ["activeTor5", 0, 1, 1, "", "Alarme inactive/active TOR 5"],
    ["activeTor6", 0, 1, 1, "", "Alarme inactive/active TOR 6"],
    ["sensTor1", 0, 1, 1, "", "Sens entrée TOR 1"],
    ["sensTor2", 0, 1, 1, "", "Sens entrée TOR 2"],
    ["sensTor3", 0, 1, 1, "", "Sens entrée TOR 3"],
    ["sensTor4", 0, 1, 1, "", "Sens entrée TOR 4"],
    ["sensTor5", 0, 1, 1, "", "Sens entrée TOR 5"],
    ["sensTor6", 0, 1, 1, "", "Sens entrée TOR 6"],
    ["delaiEnvoi", 0, 7, 1, "",
        "Délai envoi auto (0 = 10 min, 1 = 20 min, 2 = 30 min, 3 = 1h, 4 = 2h, 5 = 4h, 6 = 6h, 7 = 12h) "],
    ["delaiRepet", 10, 30, 20, "", "Délai répétition alerte"],
    ["rDeradage", 0, 31, 1, "", "Rayon déradage"],
    ["sommeil", 0, 1, 1, "", "Mode sommeil"],
    ["switchConfig", 0, 1, 1, "", "Config switch"],
]
export default numberInputParams

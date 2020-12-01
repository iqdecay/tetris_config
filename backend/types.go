package main

// This type represents the info that Sigfox sends back about a device.
type deviceInfo struct {
	//e.g. "2006-01-02 15:04:05"
	DownlinkTimestamp  string            `json:"downlinkTimestamp"`
	Acknowledged       bool              `json:"acknowledged"`
	LastAckResponse    sigfoxAckResponse `json:"lastAckResponse"`
	LastDownlinkStatus string            `json:"lastDownlinkStatus"`
	// Is also stored in the beaconConfig struct of the corresponding device
	Name string `json:"name"`
}

// Represents the full acknowledgement frame for checking into details later
type sigfoxAckResponse struct {
	Device            string `json:"device"`
	Time              string `json:"time"`
	DownlinkAck       bool   `json:"downlinkAck"`
	InfoCode          string `json:"infoCode"`
	InfoMessage       string `json:"infoMessage"`
	DownlinkOverUsage bool   `json:"downlinkOverUsage"`
}

// Represents the configuration of a device. It will be sent to the callback receiver as is.
// It also contains the name given to the device, but the field is deleted by the callback receiver
type beaconConfig struct {
	// Only fields starting with capital letter are exported
	// The field is duplicated in deviceInfo struct : frontend uses deviceInfo for display, but beaconConfig for
	// configuration
	Name             string  `json:"name"`
	SeuilMinAna30v   float32 `json:"seuilMinAna30v,string"`
	ActivMinAna30v   int     `json:"activMinAna30v,string"`
	SeuilMaxAna30v   float32 `json:"seuilMaxAna30v,string"`
	ActivMaxAna30v   int     `json:"activMaxAna30v,string"`
	SeuilMinAna100mv float32 `json:"seuilMinAna100mv,string"`
	SeuilMaxAna100mv float32 `json:"seuilMaxAna100mv,string"`
	DureeCycleFeux   int     `json:"dureeCycleFeux,string"`
	AcqPositionBase  int     `json:"acqPositionBase,string"`
	ActivMinAna100mv int     `json:"activMinAna100mv,string"`
	ActivMaxAna100mv int     `json:"activMaxAna100mv,string"`
	ActiveTor1       int     `json:"activeTor1,string"`
	ActiveTor2       int     `json:"activeTor2,string"`
	ActiveTor3       int     `json:"activeTor3,string"`
	ActiveTor4       int     `json:"activeTor4,string"`
	ActiveTor5       int     `json:"activeTor5,string"`
	ActiveTor6       int     `json:"activeTor6,string"`
	SensTor1         int     `json:"sensTor1,string"`
	SensTor2         int     `json:"sensTor2,string"`
	SensTor3         int     `json:"sensTor3,string"`
	SensTor4         int     `json:"sensTor4,string"`
	SensTor5         int     `json:"sensTor5,string"`
	SensTor6         int     `json:"sensTor6,string"`
	DelaiEnvoi       int     `json:"delaiEnvoi,string"`
	DelaiRepet       int     `json:"delaiRepet,string"`
	RDeradage        int     `json:"rDeradage,string"`
	Sommeil          int     `json:"sommeil,string"`
	SwitchConfig     int     `json:"switchConfig,string"`
	TrameReçue       int     `json:"trameReçue,string"`
}

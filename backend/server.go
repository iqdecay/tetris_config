package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)
import (
	"github.com/gorilla/mux"
)

const LOGFILENAME = "goServer.log"
const CONFIGFILENAME = "configMap.json"
const INFOFILENAME = "infoMap.json"

// This handler is useful for testing purposes only, it isn't called by the frontend or callback_receiver.
func getConfigs(w http.ResponseWriter, r *http.Request) {
	log.Printf("Received GET request on /config/")
	json.NewEncoder(w).Encode(CONFIGMAP)
}

// This handler is called by the frontend and callback_receiver to get the current configuration.
// The frontend will use it to display default values in the form.
// The callback_receiver will transmit the configuration to Sigfox.
func getConfig(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r) // Gets params
	id := params["id"]
	log.Printf("Received GET request on /config/%s", id)
	config, ok := CONFIGMAP[id]
	if ok {
		json.NewEncoder(w).Encode(config)
	} else {
		// Return error because the device doesn't have a valid configuration
		w.WriteHeader(http.StatusNotFound)
		// But create an empty configuration to be modified
		CONFIGMAP[id] = beaconConfig{}
	}
	return
}

// This handler is called by the frontend to set a new configuration for a device
func updateConfig(w http.ResponseWriter, r *http.Request) {
	// Request to this endpoint are assumed to send a full valid configuration
	// It creates a new config if the id doesn't exist yet
	params := mux.Vars(r)
	id := params["id"]
	log.Printf("Received POST request on /config/%s ", id)
	var config beaconConfig
	err := json.NewDecoder(r.Body).Decode(&config)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		errorString := fmt.Sprintf("Error decoding the JSON body : %s", err)
		log.Printf(errorString)
		json.NewEncoder(w).Encode(errorString)
	} else {
		// Valid configuration
		CONFIGMAP[id] = config
		INFOMAP[id].Name = config.Name
		json.NewEncoder(w).Encode(config)
	}
	persistToDisk()
}

// This handler is called by the frontend to display the list of devices
func getInfos(w http.ResponseWriter, r *http.Request) {
	log.Printf("Received GET request on /info/")
	json.NewEncoder(w).Encode(INFOMAP)
}

// This handler is called by the callback_receiver whenever it receives new information about a device,
// either via an acknowledgement request or a configuration request
// It creates a new deviceInfo if the id doesn't exist yet
func updateInfo(w http.ResponseWriter, r *http.Request) {
	// Request to this endpoint are assumed to send a full valid deviceInfo
	params := mux.Vars(r)
	id := params["id"]
	log.Printf("Received POST request on /info/%s ", id)
	var info *deviceInfo
	err := json.NewDecoder(r.Body).Decode(&info)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		errorString := fmt.Sprintf("Error decoding the JSON body : %s", err)
		log.Printf(errorString)
		json.NewEncoder(w).Encode(errorString)
	} else {
		// Check if name exists and copy it so it can be displayed in the frontend
		_, ok := INFOMAP[id]
		var name string
		if ok {
			name = INFOMAP[id].Name
		} else {
			name = "noName"
		}
		info.Name = name
		// Assign the new info, I guess this is a memory leak (the address is local to the scope) but it seems to work
		INFOMAP[id] = info
		json.NewEncoder(w).Encode(info)
	}
	persistToDisk()
}

// Save the maps containing the information of the system
func persistToDisk() {
	data, err := json.MarshalIndent(CONFIGMAP, "", "	")
	if err != nil {
		log.Fatalf("JSON marshaling failed: %s", err)
	}
	err = ioutil.WriteFile(CONFIGFILENAME, data, 0644)
	if err != nil {
		log.Fatalf("Saving CONFIGMAP failed : %s", err)
	}
	log.Printf("Saved CONFIGMAP to %s", CONFIGFILENAME)
	data, err = json.MarshalIndent(INFOMAP, "", "	")
	if err != nil {
		log.Fatalf("JSON marshaling failed: %s", err)
	}
	err = ioutil.WriteFile(INFOFILENAME, data, 0644)
	if err != nil {
		log.Fatalf("Saving INFOMAP failed : %s", err)
	}
	log.Printf("Saved INFOMAP to %s", INFOFILENAME)
}

// Load the maps containing the information of the system
func loadMapsFromDisk() {
	// If the file doesn't exist then the map stays empty
	_, err := os.Stat(INFOFILENAME)
	if !os.IsNotExist(err) {
		info, err := ioutil.ReadFile(INFOFILENAME)
		if err = json.Unmarshal(info, &INFOMAP); err != nil {
			log.Fatalf("JSON unmarshaling failed on %s : %s", INFOFILENAME, err)
		}
	}
	// If the file doesn't exist then the map stays empty
	_, err = os.Stat(CONFIGFILENAME)
	if !os.IsNotExist(err) {
		config, err := ioutil.ReadFile(CONFIGFILENAME)
		if err = json.Unmarshal(config, &CONFIGMAP); err != nil {
			log.Fatalf("JSON unmarshaling failed on %s : %s", CONFIGFILENAME, err)
		}
	}
}

// Apply CORS headers to a mux.Router
type HeaderDecorator struct {
	R *mux.Router
}

// Wrap the HTTP server and enable CORS headers.
func (c *HeaderDecorator) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if origin := r.Header.Get("Origin"); origin != "" {
		w.Header().Set("Access-Control-Allow-Origin", origin)
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
		w.Header().Set("Access-Control-Allow-Headers", "Accept, Accept-Language, Content-Type")
		// All responses are using JSON
		w.Header().Set("Content-Type", "application/json")
	}
	// Stop here if its Preflighted OPTIONS request
	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}
	c.R.ServeHTTP(w, r)
}

// Using global variables is *sort* of justified here because otherwise all handlers would have to be
// struct functions
var CONFIGMAP = map[string]beaconConfig{}

// The INFOMAP is a map of pointers to allow field access
var INFOMAP = map[string]*deviceInfo{}

func main() {
	var serverPort = os.Getenv("GO_PORT")
	if serverPort == "" {
		serverPort = "4000"
	}
	serverPort = ":" + serverPort
	// Fill the maps with data loaded from JSON file
	loadMapsFromDisk()
	r := mux.NewRouter()
	// If the file doesn't exist, create it or append to the file
	logFile, err := os.OpenFile(LOGFILENAME, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal(err)
	}
	mw := io.MultiWriter(os.Stdout, logFile)
	log.SetOutput(mw)
	// This endpoint is for testing only and isn't used
	r.HandleFunc("/config/", getConfigs).Methods("GET")
	// Called by the frontend for display, and callback_receiver for Sigfox transmission
	r.HandleFunc("/config/{id}/", getConfig).Methods("GET")
	// Called by the frontend to submit the configuration form
	r.HandleFunc("/config/{id}/", updateConfig).Methods("POST", "PUT")
	// Called by the frontend for display
	r.HandleFunc("/info/", getInfos).Methods("GET")
	// Called by callback_receiver with information received from Sigfox
	r.HandleFunc("/info/{id}/", updateInfo).Methods("POST", "PUT")
	// Enable CORS on the server
	decoCORS := HeaderDecorator{r}
	log.Printf("Started server on port %s", serverPort)
	log.Fatal(http.ListenAndServe(serverPort, &decoCORS))
}

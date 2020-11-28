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

const logFilename = "goServer.log"
const configFilename = "configMap.json"
const infoFilename = "infoMap.json"

// This handler is useful for testing purposes only, it isn't called by the frontend or callback receiver
func getConfigs(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	log.Printf("Received GET request on /config/")
	json.NewEncoder(w).Encode(configMap)
}

// This handler is called by the frontend and callback receiver to get the current configuration.
// The frontend will use it to display defaut values, while the callback receiver will transmit the configuration
// to Sigfox
func getConfig(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r) // Gets params
	log.Printf("Received GET request on /config/%s", params["id"])
	// Check if the parameter id is in the current configs
	config, ok := configMap[params["id"]]
	if ok {
		json.NewEncoder(w).Encode(config)
		return
	} else {
		// Return empty configuration
		json.NewEncoder(w).Encode(&beaconConfig{})
	}
}

// This handler is called by the frontend to set a new configuration for a device
func updateConfig(w http.ResponseWriter, r *http.Request) {
	// Request to this endpoint are assumed to send a full valid configuration
	// It creates a new config if the id doesn't exist yet
	w.Header().Set("Content-Type", "application/json")
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
		configMap[id] = config
		// Replicate name change
		infoMap[id].Name = config.Name
		json.NewEncoder(w).Encode(config)
	}
	// Write changes to memory
	saveMaps()
}

func getInfos(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	log.Printf("Received GET request on /info/")
	json.NewEncoder(w).Encode(infoMap)
}

func updateInfo(w http.ResponseWriter, r *http.Request) {
	// Request to this endpoint are assumed to send a full valid deviceInfo
	// It creates a new deviceInfo if the id doesn't exist yet
	w.Header().Set("Content-Type", "application/json")
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
		_, ok := infoMap[id]
		var name string
		if ok {
			name = infoMap[id].Name
		} else {
			name = "noName"
		}
		info.Name = name
		// Assign the new info, I guess this is a memory leak (the address is local to the scope) but it seems to work
		infoMap[id] = info
		json.NewEncoder(w).Encode(info)
	}
	//Write changes to memory
	saveMaps()
}

// Work on a best-effort basis : if an error occurs, still try to continue
func saveMaps() {
	// Save the configMap
	data, err := json.MarshalIndent(configMap, "", "	")
	if err != nil {
		log.Fatalf("JSON marshaling failed: %s", err)
	}
	err = ioutil.WriteFile(configFilename, data, 0600)
	if err != nil {
		log.Fatalf("Saving configMap failed : %s", err)
	}
	log.Printf("Saved configMap to %s", configFilename)
	// Save the infoMap
	data, err = json.MarshalIndent(infoMap, "", "	")
	if err != nil {
		log.Fatalf("JSON marshaling failed: %s", err)
	}
	err = ioutil.WriteFile(infoFilename, data, 0600)
	if err != nil {
		log.Fatalf("Saving infoMap failed : %s", err)
	}
	log.Printf("Saved infoMap to %s", infoFilename)
}

func loadMaps() {
	// If the file doesn't exist then the map stays empty
	_, err := os.Stat(infoFilename)
	if !os.IsNotExist(err) {
		info, err := ioutil.ReadFile(infoFilename)
		if err = json.Unmarshal(info, &infoMap); err != nil {
			log.Fatalf("JSON unmarshaling failed on %s : %s", infoFilename, err)
		}
	}
	// If the file doesn't exist then the map stays empty
	_, err = os.Stat(configFilename)
	if !os.IsNotExist(err) {
		config, err := ioutil.ReadFile(configFilename)
		if err = json.Unmarshal(config, &configMap); err != nil {
			log.Fatalf("JSON unmarshaling failed on %s : %s", configFilename, err)
		}
	}
}


// CORSRouterDecorator applies CORS headers to a mux.Router
type CORSRouterDecorator struct {
	R *mux.Router
}

// ServeHTTP wraps the HTTP server enabling CORS headers.
func (c *CORSRouterDecorator) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if origin := r.Header.Get("Origin"); origin != "" {
		w.Header().Set("Access-Control-Allow-Origin", origin)
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
		w.Header().Set("Access-Control-Allow-Headers", "Accept, Accept-Language, Content-Type")
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
var configMap = map[string]beaconConfig{}

// The infoMap is a map of pointers to allow field access
var infoMap = map[string]*deviceInfo{}

func main() {
	var serverPort = os.Getenv("GO_PORT")
	if serverPort == "" {
		serverPort = "4000"
	}
	serverPort = ":" + serverPort
	// Fill the maps with data loaded from JSON file
	loadMaps()
	r := mux.NewRouter()
	// If the file doesn't exist, create it or append to the file
	logFile, err := os.OpenFile(logFilename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal(err)
	}
	mw := io.MultiWriter(os.Stdout, logFile)
	log.SetOutput(mw)
	// This endpoint is for testing only and isn't used
	r.HandleFunc("/config/", getConfigs).Methods("GET")
	// Called by the frontend for display, and callback receiver for Sigfox transmission
	r.HandleFunc("/config/{id}/", getConfig).Methods("GET")
	// Called by the frontend to submit the configuration form
	r.HandleFunc("/config/{id}/", updateConfig).Methods("POST", "PUT")
	// Called by the frontend for display
	r.HandleFunc("/info/", getInfos).Methods("GET")
	// Called by callback receiver with information received from Sigfox
	r.HandleFunc("/info/{id}/", updateInfo).Methods("POST", "PUT")
	decoCORS := CORSRouterDecorator{r}
	log.Printf("Started server on port %s", serverPort)
	log.Fatal(http.ListenAndServe(serverPort, &decoCORS))
}

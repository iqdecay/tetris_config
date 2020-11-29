import React from "react"
import BeaconItem from "./BeaconItem"
import Navbar from "./Navbar"
import getApiUrl from "./getApiUrl";
import "../style.css"


class MainPage extends React.Component {
    // Display the list of devices detected so far, as a list of  BeaconItem cards
    constructor() {
        super();
        this.state = {
            beacons: {},
            apiCallReturned: false
        }
    }

    componentDidMount() {
        const apiUrl = getApiUrl("info")
        fetch(apiUrl, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                'Accept': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                    this.setState({beacons: data})
                }
            )
            .then(data => this.setState({apiCallReturned: true}))
            .catch(err => console.log(err))
    }

    generateBeaconsList() {
        return Object.keys(this.state.beacons).map((key, index) => {
                return <BeaconItem key={key} id={key}
                                   beacon={this.state.beacons[key]}
                />
            }
        )
    }

    render() {
        const renderBeaconsList = this.state.apiCallReturned ?
            this.generateBeaconsList() : <h1>Loading ...</h1>;
        const isEmpty = Object.keys(this.state.beacons).length ? renderBeaconsList :
            <h1>The device list is currently empty</h1>
        return (
            <div>
                <Navbar title="Sigfox supervision des balises"/>
                <div className="centered-box">
                    {isEmpty}
                </div>
            </div>
        )
    }

}

export default MainPage

import React from "react"
import BeaconItem from "./BeaconItem"
import Header from "./Header"
import beaconData from "../beaconData"
import "../style.css"


class MainPage extends React.Component {
    constructor() {
        super();
        this.state = {
            beacons: beaconData
        }
        this.handleChange = this.handleChange.bind(this)
    }

    handleChange(id) {
        this.setState((prevState) => {
            const updatedBeacons = prevState.beacons.map(beacon => {
                if (beacon.id === id) {
                    return {
                        ...beacon,
                        acknowledged: !beacon.acknowledged
                    }
                }
                return beacon
            })
            return {
                beacons: updatedBeacons
            }
        })
        console.log("Changed !", id)
    }


    render() {
        // Cool to add styling here
        const beaconsList = this.state.beacons.map(
            item => <BeaconItem key={item.id} beacon={item}
                                handleChange={this.handleChange}/>);
        return (
            <div>
                <Header title="Sigfox supervision des balises"/>
                <div className="centered-box">
                    {beaconsList}
                </div>
            </div>
        )
    }

}

export default MainPage

import React from "react"
import BeaconItem from "./BeaconItem"
import Navbar from "./Navbar"
import "../style.css"


class MainPage extends React.Component {
    constructor() {
        super();
        this.state = {
            beacons: {},
            apiCallReturned: false
        }
        this.handleChange = this.handleChange.bind(this)
    }

    componentDidMount() {
        const url = "/info/"
        fetch(url, {
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
            .then(data => console.log("Info call state : ", this.state.beacons))
            .catch(err => console.log(err))
    }

    generateBeaconsList() {
        return Object.keys(this.state.beacons).map((key, index) => {
                return <BeaconItem key={key} id={key}
                                   beacon={this.state.beacons[key]}
                                   handleChange={this.handleChange}/>
            }
        )
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
    }


    render() {
        const renderBeaconsList = this.state.apiCallReturned ?
            this.generateBeaconsList() : <h1> Loading ...</h1>
        return (
            <div>
                <Navbar title="Sigfox supervision des balises"/>
                <div className="centered-box">
                    {renderBeaconsList}
                </div>
            </div>
        )
    }

}

export default MainPage

import React from 'react';
import Navbar from "./Navbar";
import ConfigForm from "./ConfigForm";

class ConfigPage extends React.Component {
    constructor(props) {
        super();
        this.state = props.location.state
    }

    render() {
        // Get the URL parameter
        const beaconId = this.props.match.params.beaconID
        const title = `Page de configuration pour la balise
         "${this.state.beacon.name}", id = ${beaconId}`
        return (
            <div>
                <Navbar title={title} isConfigPage={true}/>
                <div className="centered-box">
                    {beaconId}
                    <ConfigForm beacon={this.state.beacon} beaconId={beaconId}/>
                </div>
            </div>
        )
    }
}

export default ConfigPage

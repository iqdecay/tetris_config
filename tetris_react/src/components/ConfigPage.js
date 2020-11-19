import React from 'react';
import Navbar from "./Navbar";
import ConfigForm from "./ConfigForm";

class ConfigPage extends React.Component {
    constructor(props) {
        super();
        this.state = props.location.state
    }

    render() {
        const title = `Page de configuration pour la balise
         "${this.state.beacon.name}", id = ${this.state.beacon.id}`
        return (
            <div>
                <Navbar title={title} isConfigPage={true}/>
                <div className="centered-box">
                    {this.props.match.params.beaconID}
                    <ConfigForm beacon={this.state.beacon}/>
                </div>
            </div>
        )
    }
}

export default ConfigPage

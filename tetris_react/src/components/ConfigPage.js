import React from 'react';
import Header from "./Header";
import TextForm from "./TextForm";

class ConfigPage extends React.Component {
    constructor(props) {
        super();
        this.state = props.location.state
        console.log(props)
    }

    render() {
        const title = `Config page for beacon "${this.state.beacon.name}"`
        return (
            <div>
                <Header title={title}/>
                <div className="centered-box">
                     {this.props.match.params.beaconID}
                    <TextForm/>
                </div>
            </div>
        )
    }
}

export default ConfigPage

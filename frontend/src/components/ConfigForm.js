import React from 'react';
import {withRouter} from 'react-router-dom';
import NumberInput from "./NumberInput";
import numberInputParams from "./numberInputParams";
import getApiUrl from "./getApiUrl";

class ConfigForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            apiCallReturned: false,
            name: this.props.beacon.name,
        }
        // Initialize all parameters in the configuration so it can be checked for validation
        for (const item of numberInputParams) {
            this.state[item[0]] = ""
        }
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleInputChange(event) {
        const target = event.target
        const value = target.value
        const name = target.name
        this.setState({
            [name]: value,
        });
    }

    handleValidation() {
        if (!this.state) {
            alert("Le formulaire est vide !")
            return false
        }
        // If only the name is filled, only the name is changed (because it is only cosmetic)
        if (this.state.name) {
            if (this.state.name.length > 32 || this.state.name.length === 0) {
                alert("Please provide a name betwenn 1 and 32 characters")
                return false
            } else {
                return true
            }
        }
        // Numerical data is "automatically" validated by HTML thanks to the min and max properties
        // Otherwise all fields must be filled
        for (const item of numberInputParams) {
            if (!this.state[item[0]]) {
                // This field's label is too long otherwise
                if (item[0] === "delaiEnvoi") {
                    alert('Le champ "Délai envoi auto" est vide')
                } else {
                    alert('Le champ "' + item[5] + '" est vide')
                }
                return false
            }
        }
        // All fields are filled, data is validated
        return true
    }

    handleSubmit(event) {
        // Submit should export the form data ONLY when it constitutes a correct Sigfox configuration
        event.preventDefault()
        if (!this.handleValidation()) {
            return
        }
        const newConfig = this.state
        delete newConfig.apiCallReturned
        newConfig.id = this.props.beaconId
        const endpoint = "config/" + this.props.beaconId
        const apiUrl = getApiUrl(endpoint)
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newConfig)
        })
            .then(response => response.json())
            .then(data => {
                const successString =
                    "Nouvelle configuration sauvegardée  pour la balise " +
                    `${this.props.beacon.name} (id ${this.props.beaconId})`
                alert(successString)
            })
            .then(this.props.history.push('/'))
            .catch(err => console.log(err))
    }

    generateFormInputs() {
        // Render one input per numerical field in the form
        return numberInputParams.map(
            item => <NumberInput name={item[0]}
                                 key={item[0]}
                                 min_val={item[1]}
                                 max_val={item[2]}
                                 step={item[3]}
                                 unit={item[4]}
                                 label={item[5]}
                                 defaultValue={this.state[item[0]]}
                                 onChange={this.handleInputChange}
            />)
    }

    componentDidMount() {
        // Get the previous configuration for this device
        const endpoint = "config/" + this.props.beaconId
        const apiUrl = getApiUrl(endpoint)
        fetch(apiUrl, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                'Accept': 'application/json',
                // "Origin": "localhost:4000",
            }
        })
            .then(response => response.json())
            .then(data => {
                    this.setState({apiCallReturned: true})
                    const oldConfig = data
                    // Now that API call returned we can set the default values to state
                    for (var key in oldConfig) {
                        this.setState({[key]: oldConfig[key]})
                    }
                }
            )
            .catch(err => console.log(err))
    }

    render() {
        const formStyle = {display: "table"}
        const renderFormInputs = this.state.apiCallReturned ?
            this.generateFormInputs() : <h1>Loading ... </h1>
        return (
            < form onSubmit={this.handleSubmit}>
                <div style={formStyle}>
                    <div className={"form-input"}>
                        <label className={"form-input"}>
                            Nom de la balise : </label>
                        <input className={"form-input"}
                               name={"name"}
                               type="text"
                               defaultValue={this.props.beacon.name}
                               onChange={this.handleInputChange}
                        />
                    </div>
                    {renderFormInputs}
                </div>
                <input type="submit" value="Submit"/>
            </form>
        );
    }
}

export default withRouter(ConfigForm)
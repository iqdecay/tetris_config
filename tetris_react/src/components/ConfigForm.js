import React from 'react';
import NumberInput from "./NumberInput";
import numberInputParams from "./numberInputParams";
import Alert from '@material-ui/lab/Alert';

class ConfigForm extends React.Component {

    constructor(props) {
        super(props);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleInputChange(event) {
        const target = event.target
        const value = target.value
        const name = target.name
        this.setState({
            [name]: value
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
        // Submit should export the form data ONLY when it is constitutes a correct Sigfox configuration
        // TODO : form data export to server (POST request to json server)
        // TODO : load previous configuration (
        // TODO : go back to main page
        // TODO :
        event.preventDefault()
        if (!this.handleValidation()) {
            return
        }

        const successString = "Nouvelle configuration sauvegardée pour la balise " +
                                `${this.props.beacon.name} (id ${this.props.beacon.id})`
        alert(successString)
    }

    render() {
        const formStyle = {display: "table"}
        const formInputs = numberInputParams.map(
            item => <NumberInput name={item[0]}
                                 key={item[0]}
                                 min_val={item[1]}
                                 max_val={item[2]}
                                 step={item[3]}
                                 unit={item[4]}
                                 label={item[5]}
                                 onChange={this.handleInputChange}
            />)
        return (
            < form onSubmit={this.handleSubmit}>
                <div style={formStyle}>
                    <div className={"form-input"}>
                        <label className={"form-input"}>
                            Nom de la balise : </label>
                        <input name={"name"}
                               type="text"
                               defaultValue={this.props.beacon.name}
                               onChange={this.handleInputChange}
                               className={formInputs}
                        />
                    </div>
                    {formInputs}
                </div>
                <input type="submit" value="Submit"/>
            </form>
        );
    }
}

export default ConfigForm
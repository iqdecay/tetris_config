import React from 'react';
import NumberInput from "./NumberInput";
import numberInputParams from "./numberInputParams";

class TextForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isGoing: true,
            numberOfGuests: 2
        };

        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });
    }

    render() {
        const form_style = {display: "table"}
        const form_inputs = numberInputParams.map(
            item => <NumberInput name={item[0]}
                                 min_val={item[1]}
                                 max_val={item[2]}
                                 step={item[3]}
                                 unit={item[4]}
                                 label={item[5]}
            />)
        // TODO : add logic for mapping each form field to its parameters
        return (
            < form style={form_style}>
                {form_inputs}
                // TODO : display the list made above
            </form>
        );
    }
}

export default TextForm
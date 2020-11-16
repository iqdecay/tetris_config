import React from 'react';
import "./NumberInput.css"

class NumberInput extends React.Component {
    constructor(props) {
        super();
    }

    render() {
        return (
            <div className="number-input">
                <label className="number-input">
                    {this.props.label}
                </label>
                <input
                    className="number-input"
                    name={this.props.name} type="number"
                    value={this.props.value}
                    max={this.props.max_val}
                    min={this.props.min_val}
                    step={this.props.step}
                    onChange={this.handleInputChange}/>
            </div>
        )
    }
}
export default NumberInput

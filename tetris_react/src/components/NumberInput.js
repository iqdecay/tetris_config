import React from 'react';
import "./NumberInput.css"

class NumberInput extends React.Component {
    constructor(props) {
        super();
        this.handleItemChange = this.handleItemChange.bind(this)
    }

    handleItemChange(event) {
        this.props.onChange(event)
    }

    render() {
        return (
            <div className="form-input">
                <label className="form-input">
                    {this.props.label}
                </label>
                <input
                    className="form-input"
                    name={this.props.name}
                    type="number"
                    value={this.props.value}
                    max={this.props.max_val}
                    min={this.props.min_val}
                    step={this.props.step}
                    onChange={this.handleItemChange}/>
            </div>
        )
    }
}

export default NumberInput

import React from 'react';
import "./NumberInput.css"

class NumberInput extends React.Component {
    constructor(props) {
        super();
        this.state = {
            inputValue: props.defaultValue
        }
        this.handleItemChange = this.handleItemChange.bind(this)
    }

    componentDidUpdate(prevProps, pState, ss) {
        if (this.props.defaultValue !== prevProps.defaultValue) {
            this.setState({inputValue: this.props.defaultValue})
        }
    }

    handleItemChange(event) {
        this.setState({inputValue: event.target.value})
        // Propagate change up
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
                    value={this.state.inputValue}
                    max={this.props.max_val}
                    min={this.props.min_val}
                    step={this.props.step}
                    onChange={this.handleItemChange}/>
            </div>
        )
    }
}

export default NumberInput

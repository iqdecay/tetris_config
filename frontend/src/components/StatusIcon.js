import React from "react";
import ErrorIcon from '@material-ui/icons/Error';
import CheckCircleRoundedIcon from '@material-ui/icons/CheckCircleRounded';

class StatusIcon extends React.Component {
    constructor(props) {
        super();
    }

    OkIcon() {
        const style = {
            fill: "green",
            fontSize: "48px",
        }
        return <CheckCircleRoundedIcon style={style}/>
    }

    ProblemIcon() {
        const style = {
            fill: "red",
            fontSize: "48px",
        }
        return <ErrorIcon style={style}/>
    }

    render() {
        const commStatus = this.props.beacon.acknowledged ? this.OkIcon() : this.ProblemIcon()
        return (
            <div className="icon">
                {commStatus}
            </div>
        )
    }
}

export default StatusIcon;

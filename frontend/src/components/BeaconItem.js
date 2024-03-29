import React from "react";
import {Link} from "react-router-dom";
import SettingsIcon from '@material-ui/icons/Settings';
import StatusIcon from "./StatusIcon";
import CustomizedDialogs from "./StatusInfo";
import "./BeaconItem.css"

class BeaconItem extends React.Component {
    /* An element representing a device, displayed as an horizontal card*/
    /* It has 3 main components :
    / - A text box with the name, id and last timestamp
    / - A box with a clickable icon to display if the acknowledgement was received
    / - A clickable icon to edit the configuration for the device
     */
    constructor(props) {
        super();
        this.state = {
            isHovered: false
        }
        this.toggleHover = this.toggleHover.bind(this)
    }

    toggleHover() {
        this.setState(prevState => ({isHovered: !prevState.isHovered}))
    }

    render() {
        const hover = this.state.isHovered && "is-hovered"
        const style = {flexGrow: 4}
        const to = {
            pathname: "/config/" + this.props.id,
            state: {beacon: this.props.beacon}
        }

        return (
            <div className={"beacon-item " + hover}
                 onMouseEnter={this.toggleHover}
                 onMouseLeave={this.toggleHover}>
                <div className={"text-box"} style={style}>
                    <h1>{this.props.beacon.name}</h1>
                    <h2>Id : {this.props.id}</h2>
                    {this.props.beacon.downlinkTimestamp}
                </div>
                <div className={"column-box status"}>
                    <StatusIcon beacon={this.props.beacon}/>
                    <CustomizedDialogs beacon={this.props.beacon} id={this.props.id}/>
                </div>
                <div className={"column-box"}>
                    <Link style={{textDecoration: "none"}} to={to}>
                        <SettingsIcon style={{fontSize: "48px", fill: "grey"}}/>
                    </Link>
                </div>
            </div>
        )
    }
}

export default BeaconItem;

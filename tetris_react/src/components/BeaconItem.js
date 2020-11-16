import React from "react";

import {Link} from "react-router-dom";
import SettingsIcon from '@material-ui/icons/Settings';


import StatusIcon from "./StatusIcon";
import "./BeaconItem.css"
import CustomizedDialogs from "./StatusInfo";

class BeaconItem extends React.Component {
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

    flexBox(int) {
        return {flexGrow: int}
    }

    render() {
        const hover = this.state.isHovered && "is-hovered"
        const style = {flexGrow: 4}
        const link = "/config/" + this.props.beacon.id
        const to = {
            pathname: "/config/" + this.props.beacon.id,
            state: {beacon: this.props.beacon}
        }

        return (
            <div className={"beacon-item " + hover}
                 onMouseEnter={this.toggleHover}
                 onMouseLeave={this.toggleHover}>
                <div className={"text-box"} style={style}>
                    <h1>{this.props.beacon.name}</h1>
                    <h2>Id : {this.props.beacon.id}</h2>
                    {this.props.beacon.last_ack_response}
                </div>
                <div className={"column-box status"}>
                    <StatusIcon beacon={this.props.beacon}/>
                    <CustomizedDialogs beacon={this.props.beacon}/>
                </div>
                <div className={"column-box"}>
                    {/*<Link style={{textDecoration: "none"}}*/}
                    {/*      to={to}>*/}
                    <SettingsIcon style={{fontSize: "48px"}}/>
                    {/*</Link>*/}
                </div>
            </div>
        )
    }
}

export default BeaconItem;
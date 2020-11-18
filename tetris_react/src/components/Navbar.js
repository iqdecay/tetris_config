import React from "react";
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import {Link} from "react-router-dom";
import "./Navbar.css"

class Navbar extends React.Component {
    constructor(props) {
        super();
    }

    render() {
        const to = {pathname: "/"}
        const buttonStyle = {
            fontSize: "48px",
            fill: "whitesmoke",
            float: "right",
        }
        const returnButton =
            <Link style={{textDecoration: "none"}}
                  to={to}>
                <ArrowBackIcon style={buttonStyle}/>
            </Link>
        const showButton = this.props.isConfigPage && returnButton
        return (
            <div>
                <header className="navbar">
                    <div className="icon-box">
                        {showButton}
                    </div>
                    <div className="title-box">
                        {this.props.title}
                    </div>
                </header>
            </div>
        )
    }
}

export default Navbar;
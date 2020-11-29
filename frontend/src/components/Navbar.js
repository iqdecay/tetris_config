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
            <div className="icon-box">
                <Link style={{textDecoration: "none"}}
                      to={to}>
                    <ArrowBackIcon style={buttonStyle}/>
                </Link>
            </div>
        const showReturnButton = this.props.isConfigPage && returnButton
        return (
            <div>
                <header className="navbar">
                    {showReturnButton}
                    <div className="title-box">
                        {this.props.title}
                    </div>
                    <div className="icon-box">
                    </div>
                </header>
            </div>
        )
    }
}

export default Navbar;
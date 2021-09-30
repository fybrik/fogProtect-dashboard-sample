import './App.css';
import React from 'react';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import FormControl from '@material-ui/core/FormControl';
import InputBase from '@material-ui/core/InputBase';
import NativeSelect from '@material-ui/core/NativeSelect';
import Typography from "@material-ui/core/Typography";
import IBMTrademark from "./ibm-logo.png";
import FogProtectTrademark from "./fogprotect-logo.png";
import HorizonTrademark from "./horizon-logo.jpg";


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <img src={IBMTrademark} alt="IBM Trademark" height="30" width="50" style={{position: "absolute", top: 0, right: 0}}/>
          <Factory />
        </div>
        <div style={{position: "absolute", bottom: 0, left: 5}}>
          <p style={{fontSize: "60%"}}>
            Based on a scenario created by BotCraft, Nagarro and Nokia in Nokia’s <br />
            “Factory in a Box” technology demonstrator developed for the EU H2020 <br />
            FogProtect project.
          </p>
          <img src={FogProtectTrademark} alt="FogProtect Trademark" height="50" width="100" />
        </div>
        <div style={{position: "absolute", bottom: 0, right: 5}}>
          <p style={{fontSize: "60%"}}>
            The research leading to these results has received funding from the European <br />
            Community’s Horizon 2020 research and innovation programme under <br />
            grant agreement n° 871525
          </p>
          <img src={HorizonTrademark} alt="Horizon Trademark" height="50" width="100" />
        </div>
      </header>
    </div>
  );
}


class Factory extends React.Component {
  constructor() {
    super();
    this.state = {
      role: "worker"
    }
    this.handleChange = this.handleChange.bind(this);
  }

  async handleChange(role) {
    await this.setState({
      role: role.target.value.toString()
    })
    console.log(this.state.role)
  }

  render() {
    return (
        <div>
          <div style={{position: "absolute", top: 10, left: 10}}>
            <Login handleChange={this.handleChange} role={this.state.role} />
          </div>
          <div style={{position: "relative", bottom: 10}}>
            <div> <ControlButton role={this.state.role} endpoint={"start_robot"} command={"Start Robot"}/> </div>
          </div>
          <div style={{position: "relative"}}>
            <div> <ControlButton role={this.state.role} endpoint={"stop_robot"} command={"Stop Robot"}/> </div>
          </div>
          <div style={{position: "relative", top: 10}}>
            <SafetyTable role={this.state.role} />
          </div>
        </div>
    )
  }
}

const BootstrapInput = withStyles((theme) => ({
  root: {
    'label + &': {
      marginTop: theme.spacing(3),
    },
  },
  input: {
    borderRadius: 4,
    position: 'relative',
    backgroundColor: theme.palette.background.paper,
    border: '1px solid #ced4da',
    fontSize: 16,
    padding: '10px 26px 10px 12px',
    transition: theme.transitions.create(['border-color', 'box-shadow']),
    // Use the system font instead of the default Roboto font.
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    '&:focus': {
      borderRadius: 4,
      borderColor: '#80bdff',
      boxShadow: '0 0 0 0.2rem rgba(0,123,255,.25)',
    },
  },
}))(InputBase);


function generateJWTToken(role) {
  let jwt = require('jsonwebtoken');

  const payload = {
    role: role
  };

  return jwt.sign(payload, process.env.JWT_KEY);
}


const restServiceIP = "127.0.0.1";
const restServicePort = "5559";

class ControlButton extends React.Component {
  constructor(props) {
    super(props);
    console.log(restServiceIP)
    this.state = {
      baseURL: "http://" + restServiceIP + ":" + restServicePort + "/api/control/",
      isLoaded: false,
      controlData: {"loading" : "loading"}
    };
  }

  async controlRequest() {
    const axios = require('axios')
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + generateJWTToken(this.props.role)
    };
    const requestURL = this.state.baseURL + this.props.endpoint
    console.log(requestURL)
    console.log(headers)

    await axios.get(requestURL, {headers}, { timeout: 10 })
        .then(response => this.setState({
          isLoaded: true,
          controlData: response.data.command,
        })).catch(error => {
          if (error.response) {
            this.setState({
              isLoaded: true,
              controlData: error.response.data
            })
          }
        })
    alert(this.state.controlData);
  };

  render() {
    return (
        <div>
          <Button variant="contained" color="primary" onClick={() => {
            this.controlRequest();
          }}>{this.props.command}</Button>
        </div>
    );
  }

}

class SafetyTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: "http://" + restServiceIP + ":" + restServicePort + "/api/personnel_data/get_safety_data",
      error: null,
      isLoaded: false,
      safetyData: {"loading" : "loading"}
    };
  }

  componentDidMount() {
    this.getRequest()
    this.interval = setInterval(() => this.getRequest(), 5000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps.role !== this.props.role) {
      this.getRequest();
    }
  }

  getRequest() {
    const axios = require('axios')
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + generateJWTToken(this.props.role)
    };

    axios.get(this.state.url, { headers }, { timeout: 10 })
        .then(response => this.setState({
          error: null,
          isLoaded: true,
          safetyData: response.data,
        }));
  }

  getRowValues(row, field) {
    const { url, error, isLoaded, safetyData } = this.state;
    if(safetyData[row] !== undefined) {
      return safetyData[row][field]
    }
  }

  render() {
    const classes = makeStyles({
      table: {
        minWidth: 650,
      },
    });

    const handleChange = async (event) => {
      await this.setState({role: event.target.value.toString()});
      this.getRequest();
    };

    const rows = {
      'Production Sector': 'production_sector',
      'Non-Production Sector': 'non_production_sector',
      'Full Area': 'full_area'
    }

    const columns = ['with_helmet', 'without_helmet', 'total']

    const column_headers = ['People with Helmet', 'People without Helmet', 'Total Number of People']

    const roles = {
      'Worker': 'worker',
      'Foreman': 'foreman',
      'HR': 'hr'
    }

    return (
        <div>
          <TableContainer component={Paper}>
            <Table className={classes.table} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell></TableCell>
                  {column_headers.map((val) =>
                      <TableCell align="center">{val}</TableCell>
                  )}
                </TableRow>
              </TableHead>
              <TableBody>
                {Object.keys(rows).map((val) =>
                    <TableRow key={val}>
                      <TableCell component="th" scope="row">
                        {val}
                      </TableCell>
                      {columns.map((column) =>
                          <TableCell align="center"> {this.getRowValues(rows[val], column)} </TableCell>
                      )}
                    </TableRow>)}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
    );
  }
}

class Login extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
  }

  render() {
    const classes = makeStyles({
      table: {
        minWidth: 650,
      },
    });

    const roles = {
      'Worker': 'worker',
      'Foreman': 'foreman',
      'HR': 'hr'
    }

    return (
        <div>
          <FormControl input={<BootstrapInput />}>
            <inputLable>
              <Typography
                  variant="subtitle1"
                  align="left"
                  color="inherit"
              >
                Role
              </Typography>
            </inputLable>
            <NativeSelect
                defaultValue="worker"
                id="role-selection"
                value={this.props.role}
                onChange={this.props.handleChange}
                input={<BootstrapInput />}
            >
              {Object.keys(roles).map((key) =>
                  <option value={roles[key]}>{key}</option>
              )}
            </NativeSelect>
          </FormControl>
        </div>
    );
  }
}

export default App;

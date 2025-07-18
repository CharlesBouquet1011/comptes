import logo from './logo.svg';
import './App.css';
import {UploadForm} from "./Analyse/analyse.jsx"
import { CSRFContext } from './VarGlob/csrf.jsx';
function App() {
  return (
    <CSRFContext>
    <div className="App">
      <UploadForm></UploadForm>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
    </CSRFContext>
  );
}

export default App;

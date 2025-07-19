import logo from './logo.svg';
import './App.css';
import {ChooseAnalyse, UploadForm} from "./Analyse/analyse.jsx"
import { CSRFContext } from './VarGlob/csrf.jsx';
function App() {
  return (
    <CSRFContext>
    <div className="App">
      <UploadForm></UploadForm>
      <ChooseAnalyse /> 
      
    </div>
    </CSRFContext>
  );
}

export default App;

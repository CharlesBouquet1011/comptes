import './App.css';
import {ChooseAnalyse, UploadForm} from "./Analyse/analyse.jsx"
import { CSRFContext } from './VarGlob/csrf.jsx';
import { AccountProvider } from './Analyse/askAccount.jsx';
function App() {
  return (
    <CSRFContext>
    <div className="App">
      <AccountProvider>
        <UploadForm></UploadForm>
      
        <ChooseAnalyse /> 
      </AccountProvider>
    </div>
    </CSRFContext>
  );
}

export default App;

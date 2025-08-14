import './App.css';
import {ChooseAnalyse, UploadForm} from "./Analyse/analyse.jsx"
import { CSRFContext } from './VarGlob/csrf.jsx';
import { AccountProvider } from './Analyse/askAccount.jsx';
function App() {
  return (
    <CSRFContext>
    <div className="App flex flex-col items-center justify-center min-h-screen px-4 bg-gray-50">
      <AccountProvider>
        
        <UploadForm />
        
        <ChooseAnalyse /> 
        
      </AccountProvider>
    </div>
    </CSRFContext>
  );
}

export default App;

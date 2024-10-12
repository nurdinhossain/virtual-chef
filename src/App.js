import './App.css';
import { TypeAnimation } from 'react-type-animation';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <TypeAnimation
        sequence={[
          '> Welcome to Virtual Chef.',
          2000, 
          '> Please choose a recipe.',
          2000
        ]}
        wrapper="span"
        speed={50}
        style={{ fontSize: '2em', display: 'inline-block' }}
        repeat={0}
      />
      </header>
    </div>
  );
}

export default App;

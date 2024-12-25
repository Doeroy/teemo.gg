import './App.css';


function SearchBar() {
    return (
        <div class="topnav">
            <input type="text" placeholder="Game Name + "></input>
      </div>
    );
  }

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Teemo.gg
        </p>
        <SearchBar />
      </header>
    </div>
  );
}

export default App;

'use strict';

// NOTE: 'React' and 'ReactDOM' are globals available because they're exposed by <script> tags in index.html.

const Hit = ({ hit }) => {
    // You can link to a specific time in a podcast by appending '#t=100' to an original_download_link, which is an .mp3 URL.
    // This provides a cheap way to link from transcript timestamps to the corresponding audio.
    let start = Math.round(hit.start);
    return (
        <div className={"hit"}>
            <p>{hit.snippet}</p>
            <span style={{display: "block", marginBottom: "1%"}}><em>{hit.speakers.join(", ")}</em></span>
            <span style={{color: "rgba(103,114,229, 0.8)", marginBottom: "1%"}}><a rel="noopener noreferrer" target="_blank" href={hit.episode_url}>{hit.episode_title}</a></span>
            {start >= 0 ? <span className={"listen-btn"}><a rel="noopener noreferrer" target="_blank" href={`${hit.original_download_link}#t=${start}`}>🎧 Listen</a></span> : null}
        </div>
    );
};

const Pane = ({contents}) => {
  return (
      <div className={"terminal space shadow"}>
          <div className="top">
              <div className="btns">
                  <span className="circle red"></span>
                  <span className="circle yellow"></span>
                  <span className="circle green"></span>
              </div>
              <div className="title">{contents}</div>
          </div>
          <pre className="body">
commands
    </pre>
      </div>
  );
};

const App = () => {
    const panes = [
        "python3 mail_server.py",
        "python3 spam_detect_server.py",
        "python3 mail_traffic_simulation.py senders",
        "python3 metrics_server.py",
        "python3 mail_traffic_simulation.py receivers",
    ];

    return (
        <div>
            <div style={{display: "flex", gap: "20px", flexBasis: "100%", flexWrap: "wrap"}}>
                {
                    panes.map(pane => <Pane contents={pane}/>)
                }
            </div>

        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('wrap'));

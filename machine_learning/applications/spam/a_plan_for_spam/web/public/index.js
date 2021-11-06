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

/**
 * A terminal pane that simulates 'tailing' a log file's output.
 *
 * @param title - String shown as the terminal window title
 * @param contents - Array of form [{timestamp: x, line: "foo ..."}, ...]
 * @returns {JSX.Element}
 */
const TerminalPane = ({title, contents}) => {
    const [index, setIndex] = React.useState(0);
    const [currentLine, setCurrentLine] = React.useState(contents[0]);
    const [visibleLines, setVisibleLines] = React.useState([]);

    React.useEffect(() => {
        setCurrentLine(contents[index]);
        setVisibleLines(oldArray => [...oldArray, contents[index]]);
    }, [index]);

    React.useEffect(() => {
        const interval = setTimeout(() => {
            setIndex(index === contents.length - 1 ? 0 : index + 1);
        }, (contents[index+1].timestamp - currentLine.timestamp) * 1000); // timeout is in milliseconds
    }, [currentLine]);

    return (
      <div className={"terminal space shadow"}>
          <div className="top">
              <div className="btns">
                  <span className="circle red"></span>
                  <span className="circle yellow"></span>
                  <span className="circle green"></span>
              </div>
              <div className="title">{title}</div>
          </div>
          <pre className="body">
              {/*{JSON.stringify(contents)}*/}
              {visibleLines.map(c => <p>{c.line}</p>)}
          </pre>
      </div>
    );
};

const App = () => {
    const fakeLogs = [
        {timestamp: 2, line: "bees cities racoon ladies men women weights bees creator girls foofighters foofighters foofighters girls man"},
        {timestamp: 3, line: "a lanes bees tyler journalists movies hell weights creator tyler tyler plants stock market men women"},
        {timestamp: 4, line: "bytes heaven racoon fooo girls weights a the tyler a fair a fair women plants"},
        {timestamp: 5, line: "hell a foofighters men the hell foofighters girls the fooo fair lanes hell weights weights"},
        {timestamp: 6, line: "heaven hell movies women men hell ladies a cities tyler hell heaven man movies heaven"},
        {timestamp: 7, line: "plants lanes houses houses movies hell plants creator racoon fooo heaven hell girls movies men"},
        {timestamp: 11, line: "man fair houses women hell men movies plants foofighters men heaven racoon bytes lanes the"},
        {timestamp: 12, line: "the plants weights bytes man movies bees the a bytes men cities fooo girls fair"},
        {timestamp: 13, line: "lanes movies movies hell tyler lanes plants journalists fooo bees man tyler heaven plants heaven"},
        {timestamp: 14, line: "man bytes plants fair lanes men journalists girls man plants houses hell girls bytes hell"},
        {timestamp: 15, line: "girls bees bytes girls man plants houses fooo tyler hell stock market houses movies weights the"},
        {timestamp: 16, line: "movies tyler hell stock market tyler houses men racoon women lanes man bees plants creator tyler"},
        {timestamp: 17, line: "cities bytes tyler girls houses stock market cities lanes journalists weights creator weights movies men ladies"},
        {timestamp: 18, line: "weights plants a houses heaven creator men man ladies stock market girls bees ladies fair heaven"},
        {timestamp: 19, line: "weights plants creator journalists journalists a fair cities man man plants girls a man lanes"},
        {timestamp: 20, line: "cities man lanes a bytes man bytes ladies houses men creator movies the women racoon"},
        {timestamp: 21, line: "foofighters bees weights journalists movies hell fooo fooo movies cities man tyler cities plants plants"},
        {timestamp: 22, line: "hell foofighters movies heaven racoon ladies man journalists ladies fooo bees cities weights tyler fair"},
        {timestamp: 23, line: "bees bytes bees weights bytes bees the bees foofighters bytes ladies creator heaven ladies man"},
        {timestamp: 24, line: "plants a houses racoon ladies houses women girls bees creator houses ladies fooo plants man"},
        {timestamp: 25, line: "hell bytes heaven houses racoon weights ladies fair houses weights man the a bees foofighters"},
        {timestamp: 26, line: "ladies houses tyler bees tyler girls racoon plants movies bytes fooo bytes movies lanes bees"},
        {timestamp: 27, line: "the lanes bees bees women the foofighters a ladies heaven movies lanes man racoon a"},
        {timestamp: 28, line: "foofighters bees girls women women foofighters movies bees movies the fooo weights movies man fooo"},
        {timestamp: 29, line: "women tyler houses bees ladies plants a movies tyler bees lanes women man fooo heaven"},
        {timestamp: 29, line: "plants fooo men cities houses movies a stock market women movies plants fooo girls cities ladies"},
        {timestamp: 29, line: "creator a a stock market fooo cities bees a fair plants man men girls journalists tyler"},
        {timestamp: 29, line: "tyler bees women plants heaven men bytes girls men heaven weights houses movies stock market foofighters"},
        {timestamp: 30, line: "plants bytes racoon tyler movies journalists racoon heaven fair foofighters the a heaven heaven man"},
        {timestamp: 31, line: "a weights bees journalists man plants movies foofighters ladies heaven a movies bees tyler fooo"},
        {timestamp: 32, line: "fair heaven stock market journalists women tyler movies stock market foofighters racoon the girls bytes a ladies"},
        {timestamp: 33, line: "plants racoon the the heaven weights creator the creator the foofighters women ladies ladies women"},
        {timestamp: 38, line: "hell a a a creator heaven fair fooo movies women bees movies lanes women cities"},
        {timestamp: 39, line: "man bytes bees lanes journalists men movies a foofighters girls cities stock market bees racoon heaven"},
        {timestamp: 45, line: "plants bees women tyler stock market man ladies women lanes tyler houses heaven cities foofighters houses"},
        {timestamp: 49, line: "the creator movies journalists tyler lanes fooo ladies plants weights weights bytes journalists weights stock market"},
        {timestamp: 53, line: "fooo movies tyler women stock market ladies men men creator plants weights weights ladies a women"},
        {timestamp: 55, line: "fooo journalists creator bytes fooo cities heaven fooo weights girls heaven stock market heaven racoon weights"},
        {timestamp: 59, line: "foofighters women women fair movies movies weights stock market fair tyler racoon racoon men bytes bees"},
        {timestamp: 60, line: "plants tyler a creator movies foofighters houses weights tyler racoon the fooo fair racoon man"},
    ];

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
                    panes.map(pane => <TerminalPane title={pane} contents={fakeLogs}/>)
                }
            </div>

        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('wrap'));

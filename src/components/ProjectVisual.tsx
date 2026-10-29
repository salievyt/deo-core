import {
  ArrowUpRight,
  LayoutDashboard,
  Users,
  Folder,
  CalendarDays,
  Search,
  Bell,
  Plus,
  ArrowDownUp,
  ArrowRight,
  Play,
} from "lucide-react";
export function ProjectVisual({
  type,
  cover,
  alt = "",
}: {
  type: string;
  cover?: string | null;
  alt?: string;
}) {
  if (cover)
    return (
      <div className="project-art cms-cover">
        <img src={cover} alt={alt} loading="lazy" />
      </div>
    );
  if (type === "crm")
    return (
      <div
        className="project-art crm-art"
        aria-label="Концепция интерфейса DEO CRM"
      >
        <div className="art-grain" />
        <div className="crm-window">
          <aside className="crm-side">
            <b>
              ✳ deo<span>crm</span>
            </b>
            <span className="workspace-avatar">
              D{" "}
              <small>
                DEO Workspace
                <br />
                <i>Pro plan⌄</i>
              </small>
            </span>
            <span className="side-active">
              <LayoutDashboard /> Overview
            </span>
            <span>
              <Users /> Clients
            </span>
            <span>
              <Folder /> Projects <em>12</em>
            </span>
            <span>
              <CalendarDays /> Calendar
            </span>
            <div className="side-bottom">✦ &nbsp; A little more organized.</div>
          </aside>
          <div className="crm-main">
            <div className="crm-top">
              Workspace <span>/</span> Overview{" "}
              <div>
                <Search />
                <Bell />
                <i>AK</i>
              </div>
            </div>
            <div className="crm-greeting">
              <div>
                <small>MONDAY, OCTOBER 12</small>
                <h4>
                  A good day to make
                  <br />
                  something great<span>✳</span>
                </h4>
              </div>
              <span className="demo-button">
                <Plus size={10} /> New project
              </span>
            </div>
            <div className="metrics">
              <div>
                <small>Total revenue ↗</small>
                <b>
                  $24,580<em>+12.8%</em>
                </b>
                <div className="spark-bars">
                  {[30, 48, 38, 65, 52, 75, 62, 89, 73, 99, 82, 110].map(
                    (h, i) => (
                      <i style={{ height: h / 3 }} key={i} />
                    ),
                  )}
                </div>
              </div>
              <div>
                <small>Active projects ↗</small>
                <b>
                  12<em>+3 this month</em>
                </b>
                <p>Moving ideas forward.</p>
                <div className="progress">
                  <i />
                </div>
              </div>
              <div>
                <small>New clients ↗</small>
                <b>
                  38<em>+8.2%</em>
                </b>
                <p>Your network is growing.</p>
                <div className="mini-avatars">
                  <i>AL</i>
                  <i>MR</i>
                  <i>JS</i>
                  <i>+5</i>
                </div>
              </div>
            </div>
            <div className="crm-projects">
              <b>
                Projects in progress <small>View all ↗</small>
              </b>
              <div className="table-head">
                <span>Project name</span>
                <span>Status</span>
                <span>Team</span>
                <span>Progress</span>
              </div>
              {[
                ["D", "DILZ Mobile App", "In progress", "76"],
                ["M", "My Exchange", "In review", "92"],
                ["O", "OK Erudit Platform", "In progress", "48"],
              ].map(([l, n, s, p]) => (
                <div className="table-row" key={n}>
                  <span>
                    <i>{l}</i>
                    {n}
                  </span>
                  <span>
                    <em>{s}</em>
                  </span>
                  <span className="table-team">● ● ●</span>
                  <span>
                    <i style={{ width: p + "%" }} />
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="art-caption">
          <span>ONE WORKSPACE. FULL CONTROL.</span>
          <span>DEO CRM ↗</span>
        </div>
      </div>
    );
  if (type === "mobile")
    return (
      <div
        className="project-art mobile-art"
        aria-label="Концепция мобильного интерфейса DILZ"
      >
        <div className="mobile-word">
          dilz<span>®</span>
        </div>
        <div className="phone phone-back">
          <div className="phone-notch" />
          <div className="phone-status">
            9:41 <span>● ▰</span>
          </div>
          <div className="phone-head">
            Discover
            <br />
            your next thing.
          </div>
          <div className="phone-circle">
            <span>✳</span>
          </div>
          <div className="phone-white">
            <small>MADE FOR YOUR EVERYDAY</small>
            <b>
              One app.
              <br />
              More possibilities.
            </b>
            <span className="phone-link">
              Explore now <ArrowUpRight size={16} />
            </span>
          </div>
        </div>
        <div className="phone phone-front">
          <div className="phone-notch" />
          <div className="phone-status">
            9:41 <span>● ▰</span>
          </div>
          <div className="phone-appbar">
            <b>dilz.</b>
            <span>☰</span>
          </div>
          <small>GOOD TO SEE YOU</small>
          <h4>
            Hello,
            <br />
            let’s explore<span>✳</span>
          </h4>
          <div className="phone-search">
            <Search size={11} /> What are you looking for?
          </div>
          <div className="phone-feature">
            <span>
              Discover something
              <br />
              <b>made for you.</b>
            </span>
            <div className="feature-orbit">✳</div>
            <span className="feature-btn">
              <ArrowUpRight size={13} />
            </span>
          </div>
          <div className="phone-categories">
            <span>Explore</span>
            <small>See all ↗</small>
          </div>
          <div className="phone-tiles">
            <div>
              ↗<small>For you</small>
            </div>
            <div>
              ✦<small>Popular</small>
            </div>
          </div>
          <div className="phone-nav">
            ⌂ <span>⊞</span> ♡ ◉
          </div>
        </div>
        <div className="art-caption">
          <span>DESIGNED AROUND YOU.</span>
          <span>MOBILE EXPERIENCE ↗</span>
        </div>
      </div>
    );
  if (type === "exchange")
    return (
      <div className="project-art exchange-art">
        <div className="exchange-window">
          <div className="exchange-top">
            <b>
              my exchange<span>↗</span>
            </b>
            <small>Overview &nbsp; Markets &nbsp; Wallet</small>
            <i>MC</i>
          </div>
          <div className="exchange-content">
            <div className="exchange-overview">
              <small>YOUR TOTAL BALANCE</small>
              <h4>
                $12,840<span>.50</span>
              </h4>
              <p>
                ↗ 4.28% <span>this month</span>
              </p>
              <div className="chart-label">
                Portfolio performance <span>1W　1M　3M　1Y</span>
              </div>
              <svg viewBox="0 0 400 140" className="chart" aria-hidden="true">
                <defs>
                  <linearGradient id="chartFill" x1="0" y1="0" x2="0" y2="1">
                    <stop stopColor="#f5caaa" stopOpacity=".4" />
                    <stop offset="1" stopColor="#f5caaa" stopOpacity="0" />
                  </linearGradient>
                </defs>
                <path
                  d="M0 120L25 105 45 115 65 87 88 97 115 60 140 79 165 65 185 74 210 45 235 52 258 32 280 46 300 20 320 30 345 15 365 25 400 6V140H0Z"
                  fill="url(#chartFill)"
                />
                <path
                  d="M0 120L25 105 45 115 65 87 88 97 115 60 140 79 165 65 185 74 210 45 235 52 258 32 280 46 300 20 320 30 345 15 365 25 400 6"
                  fill="none"
                  stroke="#f4c7a5"
                  strokeWidth="3"
                />
              </svg>
              <div className="chart-dates">
                Oct 01 <span>Oct 07</span>
                <span>Oct 14</span>
                <span>Oct 21</span>
                <span>Oct 28</span>
              </div>
            </div>
            <div className="converter">
              <b>
                Quick exchange <ArrowDownUp size={12} />
              </b>
              <small>You send</small>
              <div>
                1,000 <span>USD ⌄</span>
              </div>
              <small>You receive</small>
              <div>
                87,450 <span>KGS ⌄</span>
              </div>
              <span className="demo-button">
                Exchange now <ArrowRight size={12} />
              </span>
            </div>
          </div>
        </div>
        <div className="art-caption">
          <span>CLARITY IN EVERY NUMBER.</span>
          <span>FINTECH ↗</span>
        </div>
      </div>
    );
  return (
    <div className="project-art education-art">
      <div className="edu-shape">
        a<span>✳</span>
      </div>
      <div className="edu-window">
        <div className="edu-header">
          <b>
            ок<span>эрудит</span>
          </b>
          <small>Программы &nbsp; О школе</small>
          <span>Начать учиться ↗</span>
        </div>
        <div className="edu-body">
          <div>
            <small>ДЛЯ ТЕХ, КОМУ ИНТЕРЕСНО</small>
            <h4>
              Большие открытия
              <br />
              начинаются
              <br />с любопытства<span>✳</span>
            </h4>
            <p>
              Учимся думать. Пробуем новое.
              <br />
              Находим то, что вдохновляет.
            </p>
            <span className="demo-button">Найти свою программу ↗</span>
          </div>
          <div className="edu-cards">
            <div>
              <span>01 / Развиваем мышление</span>
              <b>
                Думай
                <br />
                шире.
              </b>
              <i>↗</i>
            </div>
            <div>
              <span>02 / Изучаем новое</span>
              <b>
                Спрашивай.
                <br />
                Исследуй.
              </b>
              <i>
                <Play size={18} />
              </i>
            </div>
          </div>
        </div>
      </div>
      <div className="art-caption">
        <span>CURIOSITY IS A SUPERPOWER.</span>
        <span>EDUCATION ↗</span>
      </div>
    </div>
  );
}

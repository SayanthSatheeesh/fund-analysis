const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  LevelFormat, PageNumber, PageBreak, Header, Footer, TabStopType, TabStopPosition
} = require('docx');
const fs = require('fs');

const BLUE_DARK  = "1F3864";
const BLUE_MID   = "2E75B6";
const BLUE_LIGHT = "D6E4F0";
const BLUE_HDR   = "2F5496";
const WHITE      = "FFFFFF";
const GRAY_LINE  = "AAAAAA";

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// Helper: section divider paragraph
function divider() {
  return new Paragraph({
    spacing: { before: 0, after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE_MID, space: 1 } },
    children: []
  });
}

// Helper: blank line
function blank(space = 120) {
  return new Paragraph({ spacing: { before: space, after: 0 }, children: [] });
}

// Helper: normal paragraph
function para(text, opts = {}) {
  return new Paragraph({
    spacing: { before: 60, after: 80, line: 280 },
    alignment: opts.center ? AlignmentType.CENTER : AlignmentType.JUSTIFIED,
    children: [new TextRun({ text, font: "Arial", size: 22, color: opts.color || "222222", bold: opts.bold || false })]
  });
}

// Helper: bullet item
function bullet(text, ref = "bullets") {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { before: 40, after: 40, line: 276 },
    children: [new TextRun({ text, font: "Arial", size: 22, color: "222222" })]
  });
}

// Helper: numbered item
function numbered(text) {
  return new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { before: 40, after: 40, line: 276 },
    children: [new TextRun({ text, font: "Arial", size: 22, color: "222222" })]
  });
}

// Helper: mixed bold/normal paragraph
function mixedPara(parts, opts = {}) {
  return new Paragraph({
    spacing: { before: 60, after: 80, line: 280 },
    alignment: AlignmentType.JUSTIFIED,
    children: parts.map(p => new TextRun({
      text: p.text, font: "Arial", size: 22,
      bold: p.bold || false, color: p.color || "222222", italics: p.italic || false
    }))
  });
}

// Helper: heading
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 280, after: 100 },
    children: [new TextRun({ text, font: "Arial", size: 30, bold: true, color: WHITE })]
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text, font: "Arial", size: 25, bold: true, color: BLUE_DARK })]
  });
}

// Header table row helper
function hdrCell(text, w, isHeader = false) {
  return new TableCell({
    borders,
    width: { size: w, type: WidthType.DXA },
    shading: { fill: isHeader ? BLUE_HDR : "EEF4FB", type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      children: [new TextRun({ text, font: "Arial", size: 21, bold: isHeader, color: isHeader ? WHITE : "111111" })]
    })]
  });
}

// TOC entry
function tocEntry(num, title, indent = false) {
  return new Paragraph({
    spacing: { before: 40, after: 40 },
    indent: indent ? { left: 400 } : {},
    children: [
      new TextRun({ text: `${num}  ${title}`, font: "Arial", size: 22, color: "222222" })
    ]
  });
}

// Reference entry
function refEntry(text) {
  return new Paragraph({
    spacing: { before: 60, after: 40, line: 276 },
    indent: { left: 360, hanging: 360 },
    children: [new TextRun({ text, font: "Arial", size: 22, color: "222222", italics: false })]
  });
}

// ============================================================
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers2",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers3",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Arial", color: WHITE },
        paragraph: {
          spacing: { before: 280, after: 100 }, outlineLevel: 0,
          shading: { fill: BLUE_HDR, type: ShadingType.CLEAR }
        }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 25, bold: true, font: "Arial", color: BLUE_DARK },
        paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 1 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            spacing: { before: 0, after: 80 },
            children: [
              new TextRun({ text: "INDUSTRY PROJECT  |  FUND INDEX ANALYSIS", font: "Arial", size: 18, bold: true, color: BLUE_HDR }),
              new TextRun({ text: "   |   Sayanth Satheesh  •  Lead College (Autonomous)", font: "Arial", size: 18, color: "888888" })
            ]
          }),
          new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE_MID, space: 1 } },
            children: []
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            border: { top: { style: BorderStyle.SINGLE, size: 4, color: BLUE_MID, space: 1 } },
            spacing: { before: 60 },
            tabStops: [{ type: TabStopType.RIGHT, position: 9000 }],
            children: [
              new TextRun({ text: "Fund Index Analysis  |  Project Report", font: "Arial", size: 17, color: "888888" }),
              new TextRun({ text: "\t", font: "Arial", size: 17 }),
              new TextRun({ text: "Page ", font: "Arial", size: 17, color: "888888" }),
              new PageNumber()
            ]
          })
        ]
      })
    },
    children: [

      // ─── COVER BLOCK ───────────────────────────────────────
      new Paragraph({
        spacing: { before: 320, after: 40 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "INDUSTRY PROJECT REPORT", font: "Arial", size: 52, bold: true, color: BLUE_DARK })]
      }),
      new Paragraph({
        spacing: { before: 0, after: 60 },
        alignment: AlignmentType.CENTER,
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: BLUE_MID, space: 4 } },
        children: [new TextRun({ text: "Fund Index Analysis  |  Automated ELT Pipeline & BI Dashboard", font: "Arial", size: 26, bold: false, color: BLUE_MID })]
      }),
      blank(200),

      // ─── PROJECT DETAIL TABLE ───────────────────────────────
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2800, 6560],
        rows: [
          new TableRow({ children: [
            new TableCell({ borders, width: { size: 2800, type: WidthType.DXA }, shading: { fill: BLUE_HDR, type: ShadingType.CLEAR }, margins: { top: 100, bottom: 100, left: 140, right: 140 },
              children: [new Paragraph({ children: [new TextRun({ text: "Industry Project Title", font: "Arial", size: 21, bold: true, color: WHITE })] })] }),
            new TableCell({ borders, width: { size: 6560, type: WidthType.DXA }, margins: { top: 100, bottom: 100, left: 140, right: 140 },
              children: [new Paragraph({ children: [new TextRun({ text: "Fund Index Analysis", font: "Arial", size: 22, bold: true, color: BLUE_DARK })] })] })
          ]}),
          new TableRow({ children: [
            hdrCell("Student Name", 2800, true),
            hdrCell("Sayanth Satheesh", 6560)
          ]}),
          new TableRow({ children: [
            hdrCell("Name of the Institute", 2800, true),
            hdrCell("Lead College (Autonomous)", 6560)
          ]}),
          new TableRow({ children: [
            hdrCell("Start Date / End Date", 2800, true),
            hdrCell("[To be filled by student]", 6560)
          ]}),
          new TableRow({ children: [
            hdrCell("Total Effort (hrs.)", 2800, true),
            hdrCell("[To be filled by student]", 6560)
          ]}),
          new TableRow({ children: [
            hdrCell("Project Environment", 2800, true),
            hdrCell("Windows Desktop, VS Code, Python Environment", 6560)
          ]}),
          new TableRow({ children: [
            hdrCell("Tools Used", 2800, true),
            hdrCell("Python, Pandas, PostgreSQL, SQLAlchemy, Streamlit, Power BI, Plotly", 6560)
          ]})
        ]
      }),
      blank(300),

      // ─── TABLE OF CONTENTS ──────────────────────────────────
      new Paragraph({
        spacing: { before: 0, after: 80 },
        children: [new TextRun({ text: "TABLE OF CONTENTS", font: "Arial", size: 28, bold: true, color: BLUE_DARK })]
      }),
      new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE_MID, space: 1 } },
        children: []
      }),
      blank(80),
      tocEntry("1.", "Acknowledgements"),
      tocEntry("2.", "Objective and Scope"),
      tocEntry("3.", "Problem Statement"),
      tocEntry("4.", "Existing Approaches"),
      tocEntry("5.", "Approach / Methodology - Tools and Technologies Used"),
      tocEntry("6.", "Workflow"),
      tocEntry("7.", "Assumptions"),
      tocEntry("8.", "Implementation"),
      tocEntry("", "Data Collection", true),
      tocEntry("", "Processing Steps", true),
      tocEntry("", "Diagrams \u2013 Charts, Tables", true),
      tocEntry("9.", "Solution Design"),
      tocEntry("10.", "Challenges & Opportunities"),
      tocEntry("11.", "Reflections on the Project"),
      tocEntry("12.", "Recommendations"),
      tocEntry("13.", "Outcome / Conclusion"),
      tocEntry("14.", "Enhancement Scope"),
      tocEntry("15.", "Link to Code and Executable File"),
      tocEntry("16.", "Research Questions and Responses"),
      tocEntry("17.", "References"),
      blank(120),

      // ─── PAGE BREAK ─────────────────────────────────────────
      new Paragraph({ children: [new PageBreak()] }),

      // ════════════════════════════════════════════════════════
      // SECTION 1: ACKNOWLEDGEMENTS
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "1.  Acknowledgements", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("I would like to express my sincere gratitude to Lead College (Autonomous) and my project guides for their continuous support and guidance throughout the duration of this industry project. Their expertise and encouragement were instrumental in shaping the architecture and implementation of the Fund Index Analysis system. I also acknowledge the open-source community for providing robust libraries such as Pandas, SQLAlchemy, and Streamlit, which formed the technical foundation of this analytical suite."),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 2: OBJECTIVE AND SCOPE
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "2.  Objective and Scope", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("The primary objective of the Fund Index Analysis project is to design and develop a fully automated, end-to-end data engineering and business intelligence pipeline. The system tracks the daily Net Asset Value (NAV) of various mutual funds and measures their performance against established market benchmarks such as NIFTY 50, NIFTY BANK, and NIFTY IT."),
      blank(40),
      para("The scope of the project encompasses the following key deliverables:", { bold: false }),
      bullet("Automated extraction of market index data and fund NAV data."),
      bullet("Data cleaning, standardization, and quality gate enforcement."),
      bullet("Transformation of raw data into a Star Schema data mart (dimension and fact tables) hosted on a PostgreSQL database."),
      bullet("Calculation of key financial metrics, including period returns, tracking error, and deviation (Alpha)."),
      bullet("Presentation of insights through an interactive, Python-based Streamlit dashboard and Power BI templates."),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 3: PROBLEM STATEMENT
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "3.  Problem Statement", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("Investors and financial analysts frequently struggle to compare the performance of mutual funds against their respective benchmark indices due to fragmented data sources, inconsistent formatting, and the latency of manual reporting. Without a centralized, automated system to calculate tracking errors, period returns (1M, 3M, 1Y), and rolling returns, stakeholders cannot efficiently identify underperforming funds or assess true risk-adjusted returns (Alpha)."),
      blank(40),
      para("There is a critical need for an automated data pipeline that continuously ingests daily market data, processes it into a reliable data warehouse, and serves real-time visualizations for data-driven decision-making."),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 4: EXISTING APPROACHES
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "4.  Existing Approaches", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("Traditional approaches to fund index analysis generally fall into two categories:"),
      blank(40),
      mixedPara([{ text: "1.  Manual Spreadsheet Analysis: ", bold: true }, { text: "Financial analysts manually download historical CSV files from stock exchanges and fund houses, compiling them into Excel. This approach is highly prone to human error, lacks scalability, and fails to provide real-time insights." }]),
      blank(40),
      mixedPara([{ text: "2.  Proprietary Institutional Software: ", bold: true }, { text: "Large financial institutions utilize expensive tools like Bloomberg Terminals or Morningstar Direct. While powerful, these systems are cost-prohibitive for individual analysts or small firms and lack the flexibility required for custom data engineering pipelines." }]),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 5: APPROACH / METHODOLOGY
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "5.  Approach / Methodology \u2013 Tools and Technologies Used", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("This project adopts a modern Data Engineering methodology, utilizing an ELT (Extract, Load, Transform) architecture combined with a customized Business Intelligence semantic layer. The methodology focuses on modularity, utilizing distinct scripts for extraction, transformation, and visualization, ensuring that each component can be scaled or modified independently."),
      blank(60),

      // Tools table
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2200, 7160],
        rows: [
          new TableRow({ children: [
            new TableCell({ borders, width: { size: 2200, type: WidthType.DXA }, shading: { fill: BLUE_HDR, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "Category", font: "Arial", size: 21, bold: true, color: WHITE })] })] }),
            new TableCell({ borders, width: { size: 7160, type: WidthType.DXA }, shading: { fill: BLUE_HDR, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "Tool / Technology", font: "Arial", size: 21, bold: true, color: WHITE })] })] })
          ]}),
          ...([
            ["Programming Language", "Python (Core logic, pipeline orchestration)"],
            ["Data Processing", "Pandas, NumPy \u2013 Data cleaning, statistical calculations"],
            ["Database Architecture", "PostgreSQL (Relational Data Mart), SQLAlchemy (ORM and query execution)"],
            ["Visualization", "Streamlit, Plotly (Automated web dashboard), Power BI (GUI-based reporting)"],
            ["Environment & Config", "dotenv (Configuration management), VS Code, Windows Desktop"],
          ].map((row, i) => new TableRow({ children: [
            new TableCell({ borders, width: { size: 2200, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "EEF4FB" : WHITE, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: row[0], font: "Arial", size: 21, bold: true, color: BLUE_DARK })] })] }),
            new TableCell({ borders, width: { size: 7160, type: WidthType.DXA }, shading: { fill: i % 2 === 0 ? "EEF4FB" : WHITE, type: ShadingType.CLEAR }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: row[1], font: "Arial", size: 21, color: "222222" })] })] })
          ]})))
        ]
      }),
      blank(80),

      // ════════════════════════════════════════════════════════
      // SECTION 6: WORKFLOW
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "6.  Workflow", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      ...([
        ["Step 1 \u2013 Orchestration:", "The master script (run_all.py) triggers the daily execution cycle, coordinating all downstream pipeline stages."],
        ["Step 2 \u2013 Data Extraction:", "Mock data generators simulate daily closing prices and volumes for major indices (NIFTY 50) and fund NAVs, tracking watermarks to ensure only incremental data is loaded."],
        ["Step 3 \u2013 Data Quality Gate:", "Extracted data passes through a quality validation layer. Records failing validation (e.g., missing prices) are logged to the dq_audit_log table."],
        ["Step 4 \u2013 Data Mart Loading:", "Cleaned data is upserted into a PostgreSQL Star Schema. Slowly Changing Dimensions (SCD) are handled in dim_fund and dim_index, while daily prices populate fact_nav_history."],
        ["Step 5 \u2013 Aggregation:", "SQL views and Python scripts calculate rolling returns, watch list status, and period performance metrics."],
        ["Step 6 \u2013 Visualization:", "The Streamlit dashboard queries the PostgreSQL views in real-time to render dual-axis charts, KPI cards, and performance matrices."],
      ].map(([label, text]) => mixedPara([{ text: `${label}  `, bold: true }, { text }], {}))),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 7: ASSUMPTIONS
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "7.  Assumptions", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      bullet("Data Availability: Simulated data is assumed to accurately reflect the statistical behavior (random walk volatility) of actual NSE/BSE stock indices."),
      bullet("Trading Days: The system assumes a standard 5-day business week for index trading, handling missing weekend dates via forward-fill techniques if necessary."),
      bullet("Database Concurrency: PostgreSQL is assumed to be running locally on the standard port (5432) to facilitate the Streamlit application\u2019s real-time queries."),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 8: IMPLEMENTATION
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "8.  Implementation", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),

      new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 160, after: 60 }, children: [new TextRun({ text: "8.1  Data Collection", font: "Arial", size: 25, bold: true, color: BLUE_DARK })] }),
      para("Data collection is handled via Python extraction scripts. For the purpose of this project environment, realistic OHLCV (Open, High, Low, Close, Volume) data is generated dynamically using NumPy\u2019s random normal distribution to simulate market volatility (nse_index.py). The pipeline implements a \u201Cwatermark\u201D table to track the last_processed_date for each entity, ensuring that subsequent pipeline runs only extract and append new daily records rather than reprocessing historical data."),
      blank(40),

      new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 160, after: 60 }, children: [new TextRun({ text: "8.2  Processing Steps", font: "Arial", size: 25, bold: true, color: BLUE_DARK })] }),
      numbered("Staging: Raw data is loaded into stg_index_raw and stg_fund_raw staging tables."),
      numbered("Cleaning: Null values are handled, and currencies are standardized across all records."),
      numbered("Dimension Loading: Data is inserted into dim_index, dim_fund, and a pre-generated dim_date table."),
      numbered("Fact Loading: The fact_nav_history table joins funds, indices, and dates, calculating the precise daily_return and index_daily_return."),
      numbered("Business Logic: The watch_list table is populated by flagging funds that exhibit consecutive periods of negative Alpha against their benchmark."),
      blank(40),

      new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 160, after: 60 }, children: [new TextRun({ text: "8.3  Diagrams \u2013 Charts, Tables", font: "Arial", size: 25, bold: true, color: BLUE_DARK })] }),
      para("The following visualizations form the core of the Streamlit dashboard and Power BI report. Screenshots of the live dashboard should be inserted below in the final PDF submission."),
      blank(40),
      bullet("Figure 1: Dual-Axis Line Chart comparing Fund NAV vs. Index Price over the 1-year time period."),
      bullet("Figure 2: Clustered Bar Chart illustrating 1M, 3M, and 1Y period returns for all tracked funds."),
      bullet("Table 1: Multi-Fund Matrix showcasing conditionally formatted (Red/Green) monthly returns."),
      blank(40),

      // Placeholder table for Figure 1
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [9360],
        rows: [
          new TableRow({ children: [new TableCell({
            borders,
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: "F0F4F9", type: ShadingType.CLEAR },
            margins: { top: 200, bottom: 200, left: 200, right: 200 },
            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "[Figure 1: Insert Streamlit Dashboard Screenshot \u2013 Fund NAV vs. Index Dual-Axis Chart]", font: "Arial", size: 20, italics: true, color: "888888" })] })]
          })] })
        ]
      }),
      blank(80),

      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 9: SOLUTION DESIGN
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "9.  Solution Design", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("The solution is designed around a strict Star Schema database model to optimize read performance for the Business Intelligence layer. The schema separates transactional fact data from descriptive dimension data, enabling efficient analytical queries."),
      blank(40),
      mixedPara([{ text: "Central Fact Table: ", bold: true }, { text: "fact_nav_history \u2013 Stores daily prices and tracking errors." }]),
      mixedPara([{ text: "Dimension Tables: ", bold: true }, { text: "dim_fund (fund metadata and expense ratios), dim_index (benchmark details), and dim_date (year, quarter, and month hierarchies)." }]),
      mixedPara([{ text: "Semantic Views: ", bold: true }, { text: "To decouple the BI layer from the raw tables, three SQL views were created: v_trend_history, v_period_performance, and v_monthly_comparison. The Streamlit application queries only these views." }]),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 10: CHALLENGES & OPPORTUNITIES
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "10.  Challenges & Opportunities", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 100, after: 60 }, children: [new TextRun({ text: "Challenges", font: "Arial", size: 24, bold: true, color: BLUE_DARK })] }),
      bullet("Database Migration: Initially built on SQLite, the system faced file-locking constraints when attempting to run the ETL pipeline and dashboard concurrently. This was resolved by migrating the entire schema to PostgreSQL, which natively supports high concurrency."),
      bullet("Calculation Complexity: Accurately calculating rolling returns and standard deviation (Tracking Error) required complex SQL window functions and Pandas aggregations."),
      blank(40),
      new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 100, after: 60 }, children: [new TextRun({ text: "Opportunities", font: "Arial", size: 24, bold: true, color: BLUE_DARK })] }),
      bullet("The current architecture is highly scalable. Mock data generators can be seamlessly replaced with live API integrations (e.g., NSE API, Yahoo Finance) without altering the downstream data mart or dashboard."),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 11: REFLECTIONS
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "11.  Reflections on the Project", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("Developing the Fund Index Analysis system provided profound insights into the intersection of software engineering and financial analytics. Building the data pipeline underscored the importance of robust data modeling, specifically the implementation of Star Schemas and SCD Type 2 dimensions. Transitioning from a manual Power BI methodology to a fully automated Streamlit web application highlighted the immense efficiency gains of \u201CDashboard-as-Code,\u201D allowing for instant, reproducible deployments."),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 12: RECOMMENDATIONS
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "12.  Recommendations", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("For institutions looking to adopt this framework, the following recommendations are proposed:"),
      blank(40),
      new Paragraph({ numbering: { reference: "numbers2", level: 0 }, spacing: { before: 40, after: 40, line: 276 }, children: [new TextRun({ text: "Deploy the PostgreSQL database to a managed cloud instance (e.g., AWS RDS) to ensure high availability and automatic backups.", font: "Arial", size: 22 })] }),
      new Paragraph({ numbering: { reference: "numbers2", level: 0 }, spacing: { before: 40, after: 40, line: 276 }, children: [new TextRun({ text: "Implement Airflow or cron jobs to trigger the run_all.py script automatically at the close of trading hours.", font: "Arial", size: 22 })] }),
      new Paragraph({ numbering: { reference: "numbers2", level: 0 }, spacing: { before: 40, after: 40, line: 276 }, children: [new TextRun({ text: "Integrate live financial APIs to replace the staging mock data generators for real-world trading utility.", font: "Arial", size: 22 })] }),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 13: OUTCOME / CONCLUSION
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "13.  Outcome / Conclusion", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("The project successfully delivered a robust, automated Fund Index Analysis suite. By replacing manual spreadsheet exports with a Python-driven ELT pipeline, the system guarantees accurate, daily updates to fund performance metrics. The implementation of a PostgreSQL data mart integrated with a custom Streamlit dashboard provides stakeholders with immediate, actionable insights into fund deviation, tracking errors, and historical trends. The final product successfully tracks mock NIFTY indices with high precision, demonstrating the full viability of the proposed architecture for real-world financial analytics."),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 14: ENHANCEMENT SCOPE
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "14.  Enhancement Scope", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      para("Future iterations of this project could incorporate the following enhancements:"),
      blank(40),
      mixedPara([{ text: "Machine Learning Integration: ", bold: true }, { text: "Applying ARIMA or LSTM models to predict short-term NAV trends based on historical index momentum." }]),
      blank(20),
      mixedPara([{ text: "Automated Alerting: ", bold: true }, { text: "Configuring SMTP integrations to email stakeholders automatically when a fund is added to the \u201CWatch List\u201D due to severe underperformance." }]),
      blank(20),
      mixedPara([{ text: "Multi-Currency Support: ", bold: true }, { text: "Expanding the dim_fund logic to handle international ETFs requiring currency conversion rates." }]),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 15: LINK TO CODE
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "15.  Link to Code and Executable File", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      mixedPara([{ text: "Local Repository: ", bold: true }, { text: "C:\\MERN PROJECTS\\tcs-fund-analysis" }]),
      blank(20),
      mixedPara([{ text: "ETL Execution Command: ", bold: true }, { text: "python pipeline/run_all.py" }]),
      blank(20),
      mixedPara([{ text: "Dashboard Launch Command: ", bold: true }, { text: "streamlit run dashboard/app.py" }]),
      blank(20),
      mixedPara([{ text: "GitHub Repository URL: ", bold: true }, { text: "[Add GitHub URL here before final submission]", italic: true }]),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 16: RESEARCH Q&A
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "16.  Research Questions and Responses", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [9360],
        rows: [
          new TableRow({ children: [new TableCell({
            borders,
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: "EEF4FB", type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 160, right: 160 },
            children: [
              new Paragraph({ spacing: { before: 0, after: 60 }, children: [new TextRun({ text: "Q1: Why was PostgreSQL chosen over the initial SQLite implementation?", font: "Arial", size: 22, bold: true, color: BLUE_DARK })] }),
              new Paragraph({ spacing: { before: 0, after: 0 }, children: [new TextRun({ text: "SQLite relies on file-level locks during write operations. When the data pipeline was updating historical records while the dashboard was concurrently querying data, it caused database locking errors. PostgreSQL, being a true client-server RDBMS, handles high-volume concurrent reads and writes efficiently, making it the appropriate choice for this multi-process architecture.", font: "Arial", size: 22, color: "333333" })] })
            ]
          })] }),
          new TableRow({ children: [new TableCell({
            borders,
            width: { size: 9360, type: WidthType.DXA },
            margins: { top: 120, bottom: 120, left: 160, right: 160 },
            children: [
              new Paragraph({ spacing: { before: 0, after: 60 }, children: [new TextRun({ text: "Q2: How does the system calculate the Tracking Error of a fund?", font: "Arial", size: 22, bold: true, color: BLUE_DARK })] }),
              new Paragraph({ spacing: { before: 0, after: 0 }, children: [new TextRun({ text: "Tracking Error is calculated by taking the standard deviation of the daily differences in returns between the mutual fund and its benchmark index over a specific period. This metric demonstrates how closely the fund mimics the index\u2019s volatility \u2014 a lower tracking error indicates a tighter correlation to the benchmark.", font: "Arial", size: 22, color: "333333" })] })
            ]
          })] })
        ]
      }),
      blank(60),

      // ════════════════════════════════════════════════════════
      // SECTION 17: REFERENCES
      // ════════════════════════════════════════════════════════
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 240, after: 100 },
        shading: { fill: BLUE_HDR, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "17.  References", font: "Arial", size: 30, bold: true, color: WHITE })]
      }),
      blank(60),
      refEntry("McKinney, W. (2012). Python for Data Analysis. O\u2019Reilly Media."),
      refEntry("Kimball, R., & Ross, M. (2013). The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling. Wiley."),
      refEntry("Streamlit Documentation. (2026). Streamlit library for Python. Retrieved from https://streamlit.io"),
      refEntry("PostgreSQL Global Development Group. (2026). PostgreSQL 16 Documentation. Retrieved from https://www.postgresql.org/docs/"),
      refEntry("National Stock Exchange of India (NSE). Official Documentation on Index Calculation Methodology."),
      blank(120),

      // END
      new Paragraph({
        alignment: AlignmentType.CENTER,
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: BLUE_MID, space: 4 } },
        spacing: { before: 60, after: 0 },
        children: [new TextRun({ text: "End of Report  \u2014  Fund Index Analysis  |  Sayanth Satheesh  |  Lead College (Autonomous)", font: "Arial", size: 19, italics: true, color: "888888" })]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/claude/Fund_Index_Analysis_Report.docx", buf);
  console.log("Done.");
});
# Diagram authoring guide (Phase 5)

You are producing draw.io diagram sources for a personal engineering wiki at /Users/Hemant.Kumar@finova.tech/workspace/messup-learn. Do NOT edit any file in the repo. Write each diagram as a `.drawio` file (draw.io / mxGraph XML) into /private/tmp/claude-502/-Users-Hemant-Kumar-finova-tech-workspace-messup-learn/c3da6c82-d248-4143-851f-b51024f013b1/scratchpad/diagrams/ and a manifest as described below. The orchestrator exports them to `.drawio.svg` with the draw.io CLI and embeds them.

Read the target page first (path in your assignment). The diagram must match the page's corrected text, not the old picture it replaces. Every label in the diagram must be a term the page uses.

## What makes a good diagram here

- One idea per diagram. If you need more than about 25 shapes, you are drawing two diagrams.
- Labels are short nouns or one-line phrases. No sentences inside boxes. Explanation lives in the page and in the alt text.
- Left to right or top to bottom flow. Arrows mean "then" or "talks to"; label an arrow only when the reader would otherwise ask "how".
- No product logos, no icons, no clip art. Plain boxes, a few rounded, one or two colours.
- The diagram must read in both light and dark themes: black text on light fills, dark strokes.

## Palette and style (use exactly these)

- Neutral box: `rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;fontFamily=Helvetica;fontSize=12;`
- Primary box (the thing the diagram is about): `rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;fontFamily=Helvetica;fontSize=12;`
- Secondary box (data, storage, external party): `rounded=1;whiteSpace=wrap;html=1;fillColor=#D5E8D4;strokeColor=#82B366;fontFamily=Helvetica;fontSize=12;`
- Warning or failure box: `rounded=1;whiteSpace=wrap;html=1;fillColor=#F8CECC;strokeColor=#B85450;fontFamily=Helvetica;fontSize=12;`
- Container / grouping (a node, a VPC, a trust boundary): `rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#666666;dashed=1;fontFamily=Helvetica;fontSize=12;verticalAlign=top;fontStyle=1;`
- Arrow: `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;fontFamily=Helvetica;fontSize=11;endArrow=block;endFill=1;`
- Free text / caption: `text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;fontFamily=Helvetica;fontSize=11;fontColor=#333333;`
- Canvas: keep all shapes within x 0 to 1000, y 0 to 700. Minimum box 120 x 40. Leave 20 px between boxes.

## File template

```xml
<mxfile host="app.diagrams.net" modified="2026-09-16T00:00:00.000Z" agent="wiki" version="24.0.0">
  <diagram id="d1" name="Page-1">
    <mxGraphModel dx="1000" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1000" pageHeight="700" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="box1" value="Client" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="box2" value="Server" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="40" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="e1" value="request" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;fontFamily=Helvetica;fontSize=11;endArrow=block;endFill=1;" edge="1" parent="1" source="box1" target="box2">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Rules for the XML: every `id` unique; every vertex has `vertex="1" parent="1"` and an `mxGeometry` with `as="geometry"`; every edge has `edge="1" parent="1" source="..." target="..."` and `<mxGeometry relative="1" as="geometry"/>`; escape `&`, `<`, `>` and quotes in values (`&amp;`, `&lt;`, `&gt;`, `&quot;`); use `&lt;br&gt;` for a line break inside a label. Validate each file with `python3 -c "import xml.etree.ElementTree as E; E.parse('FILE')"` before finishing. One diagram per file, one page per file.

## Manifest

Append one entry per diagram to /private/tmp/claude-502/-Users-Hemant-Kumar-finova-tech-workspace-messup-learn/c3da6c82-d248-4143-851f-b51024f013b1/scratchpad/diagrams/manifest-<your-set>.yaml:

```yaml
- file: consistency-ladder.drawio          # in scratchpad/diagrams/
  page: data/Consistency Models.md          # repo path
  replaces: consistency-models.PNG          # existing image filename to remove, or null
  after_heading: "## Weaker models"         # embed the image directly after this heading's first paragraph; or after_line_containing: "exact text"
  alt: "Ladder of consistency models from strongest to weakest: linearizability (with strict serializability for transactions), sequential, causal, PRAM, eventual"
  title: "Consistency models, strong to weak"
```

The alt text is a full sentence describing what the picture shows, written for someone who cannot see it. It is not the filename.

## Report

Return: the list of files written with one line on what each shows, any label you were unsure of, and any diagram you decided not to draw and why.

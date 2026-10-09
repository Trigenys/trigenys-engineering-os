import { createServiceServer } from "./server.js";

const port = Number.parseInt(process.env.PORT || "3000", 10);
const host = process.env.HOST || "0.0.0.0";

const server = createServiceServer({
  name: "trigenys-engineering-os",
  version: "0.1.0"
});

server.listen(port, host, () => {
  console.log(JSON.stringify({
    level: "info",
    event: "service.started",
    service: "trigenys-engineering-os",
    host,
    port
  }));
});

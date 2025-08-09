# Stratus, infrastructure for a multi-tenant Platform-as-a-Service system.

Stratus provides a platform for running containerized apps on shared infrastructure. More coming soon.

This README is a work in progress.

## Abstrations/Services

- `API`: Main service API i.e access point into the system. End users will send requests to this service.
- `Management Plane`: An internal service that manages *Deployment Nodes*. Used by the *API* to create and manage deployments.
- `Deployment Node(s)`: Bare metal or virtualized servers which will run user applications in containers. Will always run an instance of *Deployment Node Agent*.
- `Deployment Node Agent`: An agent/software running on Deployment Nodes that is used to communicate with the *Management Plane*.

## How to run


**Deployment Node Agent**

```bash
cd deploy-node-agent
go run cmd/main.go
```

**API**

Copy `.env.example` to `.env` and set up the credentials
```bash
python3 -m api
```

**Management Plane**

Copy `config.example.json` to `config.json` and set up Deployment Node hosts.
Make sure those Deployment Nodes have Agents running before you start the Management Plane

```bash
python3 -m management-plane
```

**Web Frontend**

```bash
cd web-frontend
yarn # Install dependencies
yarn dev
```


## License
This project is licensed under the AGPL-3.0 License - see the LICENSE file for details.
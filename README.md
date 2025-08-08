# Stratus, an open-source Application Deployment System

Stratus provides infrastructure for a multi-tenant Platform-as-a-Service system. More coming soon.

This README is a work in progress.

## Abstrations/Services

- `API`: Main service API i.e access point into the system. End users will send requests to this service.
- `Management Plane`: An internal service that manages *Deployment Nodes*. Used by the *API* to create and manage deployments.
- `Deployment Node(s)`: Bare metal or virtualized servers which will run user applications in containers. Will always run an instance of *Deployment Node Agent*.
- `Deployment Node Agent`: An agent/software running on Deployment Nodes that is used to communicate with the *Management Plane*.

## License
This project is licensed under the AGPL-3.0 License - see the LICENSE file for details.
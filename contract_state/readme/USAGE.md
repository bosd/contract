A new contract starts in **Draft**. Use *Activate* once it should start
running; invoices are generated from that point on. *Cancel* marks a contract
that will never run.

Contracts that already existed when this module was installed are set to
**Active**, so installing it never stops invoicing that was already happening.

## Extending

The states are a plain selection, so another module can add its own with
`selection_add`, for instance a *Sent* state between draft and active for
contracts that go out to the customer to be signed.

Two hooks keep that additive rather than invasive:

- `_get_invoiceable_states()` returns the states in which a contract may
  invoice. Override it if a state you add should also invoice. Both the
  button visibility and the cron domain read it, so there is one place to
  change.
- The portal record rule excludes draft rather than allowing active, so any
  state you add is visible to the customer without touching security.

This field is the *document workflow* state, in the sense `sale.order.state`
is. It is deliberately not an aggregation of the contract line lifecycle
(`upcoming`, `to-renew`, `closed`…), which is a different question and belongs
in a field of its own.

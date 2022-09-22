import { setValue } from "./client-db";

export function saveAndSendData(elOrKey, value) {
  setValue(elOrKey, value);
  let dataCollectionURL = "{{ config.extra.telemetry_url }}";
  // TODO: fetch POST with token
}

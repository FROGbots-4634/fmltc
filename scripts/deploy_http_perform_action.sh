if [[ "${FMLTC_GCLOUD_PROJECT_ID}" == "" ]]; then
  echo "ERROR: environment is not setup correctly. Please run 'source env_setup.sh'."
  exit 1
fi


gcloud functions deploy http_perform_action \
    --runtime python37 \
    --trigger-http

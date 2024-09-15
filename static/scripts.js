document.addEventListener("DOMContentLoaded", function() {
    const clientDropdown = document.getElementById('client') || document.getElementById('client_for_deleting_campaign') || document.getElementById('client_for_adding_campaign');
    
    if (clientDropdown) {
        clientDropdown.addEventListener('change', function() {
            const client = this.value;

            // Fetch campaigns for the selected client
            fetch(`/admin/get_campaigns/${client}`)
                .then(response => response.json())
                .then(data => {
                    const campaignSelect = document.getElementById('campaign') || document.getElementById('campaign_select');
                    if (campaignSelect) {
                        campaignSelect.innerHTML = '<option value="" disabled selected>Select Campaign</option>';

                        // Populate campaigns dropdown
                        data.forEach(campaign => {
                            const option = document.createElement('option');
                            option.value = campaign;
                            option.textContent = campaign;
                            campaignSelect.appendChild(option);
                        });
                    }
                })
                .catch(error => console.error('Error fetching campaigns:', error));
        });
    } else {
        console.error("Client dropdown not found in the DOM.");
    }
});

document.getElementById('check').addEventListener('click', (e) => {
    e.preventDefault();
    const domainName = document.getElementById('domain').value;
    fetch(`/check/${domainName}`).then(res => res.json()).then(({is_valid, data}) => {
        document.getElementById('caption').textContent = domainName;
        document.getElementById('subdomain').textContent = data ? data.subdomain : null;
        document.getElementById('rootdomain').textContent = data ? data.root_domain : null;
        document.getElementById('etld').textContent = data ? data.etld : null;
        document.getElementById('tld').textContent = data ? data.tld : null;
    });
});

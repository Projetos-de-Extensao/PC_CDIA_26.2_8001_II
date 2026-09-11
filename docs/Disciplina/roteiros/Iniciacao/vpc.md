Atividade: Aula expositiva e dialogada sobre componentes de VPC.
Tópico	Descrição	Exemplos Práticos
1. O que é uma VPC?	Rede virtual privada na AWS, logicamente isolada.	VPC com CIDR 10.0.0.0/16.
2. Sub-redes	Divisões da VPC em zonas de disponibilidade. Públicas x Privadas.	Sub-rede pública (10.0.1.0/24) e privada (10.0.2.0/24).
3. Internet Gateway (IGW)	Permite comunicação da VPC com a Internet.	IGW anexado à VPC.
4. NAT Gateway	Permite que instâncias privadas acessem a Internet (atualizações, patches).	NAT Gateway na sub-rede pública.
5. Route Tables	Tabelas de roteamento que definem o tráfego.	Tabela pública: 0.0.0.0/0 → IGW. Tabela privada: 0.0.0.0/0 → NAT.
6. Security Groups	Firewall a nível de instância (regras de entrada/saída).	SG para Web: portas 80, 443. SG para DB: porta 5432 (apenas do SG Web).
7. Network ACLs (NACLs)	Firewall a nível de sub-rede (regras numeradas).	NACL pública: permite tráfego efêmero. NACL privada: mais restrita.
8. VPC Peering	Conexão entre VPCs (mesma ou diferente conta/região).	VPC Peering para comunicação entre ambientes.
9. VPN/ Direct Connect	Conexão segura com datacenter on-premises.	Cenário híbrido.


import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:share_plus/share_plus.dart';

import 'theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const AzaiApp());
}

const String limitation =
    'AZAI companion. Ask Jeeves, read receipts, view integrity, seal runtime, '
    'export/share text. Constitutional edits are blocked. Deep settings, key '
    'rotation, and vault export are blocked. The engine is the desktop azai '
    'package on 127.0.0.1:8860. Jeeves is not sovereign. Not a new foundation '
    'model. Hosted /v1 is lamb-check only, never a paid-key proxy.';

class AzaiApp extends StatelessWidget {
  const AzaiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AZAI',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: const AzaiHome(),
    );
  }
}

class AzaiHome extends StatefulWidget {
  const AzaiHome({super.key});

  @override
  State<AzaiHome> createState() => _AzaiHomeState();
}

class _AzaiHomeState extends State<AzaiHome> {
  final _prompt = TextEditingController();
  String _runtime = 'OPEN';
  String _lamb = 'PASS';
  final List<String> _receipts = <String>[
    '(connect to desktop azai serve to live-tail receipts)',
  ];
  final List<String> _chat = <String>[
    'Jeeves is ready. All output remains subordinate to Lamb Lens.',
  ];

  @override
  void dispose() {
    _prompt.dispose();
    super.dispose();
  }

  String _exportMarkdown() {
    final buf = StringBuffer();
    buf.writeln('# AZAI conversation');
    buf.writeln();
    buf.writeln('Jeeves is not sovereign. Lamb Lens governs every turn.');
    buf.writeln();
    buf.writeln('## Chat');
    buf.writeln();
    for (final row in _chat) {
      buf.writeln(row);
      buf.writeln();
    }
    buf.writeln('## Receipts');
    buf.writeln();
    for (final row in _receipts.take(12)) {
      buf.writeln('- $row');
    }
    buf.writeln();
    buf.writeln('_Apache-2.0, Aziel Eliab. Companion export, v0.3.1._');
    return buf.toString();
  }

  void _ask() {
    final text = _prompt.text.trim();
    if (text.isEmpty) return;
    setState(() {
      _chat.add('you: $text');
      _chat.add(
        'Jeeves (companion placeholder): desktop engine is azai serve. '
        'This phone does not edit the constitution.',
      );
      _receipts.insert(0, 'ask | SESSION | companion');
      _prompt.clear();
    });
  }

  void _seal() {
    setState(() {
      _runtime = _runtime == 'SEALED' ? 'OPEN' : 'SEALED';
      _receipts.insert(0, _runtime == 'SEALED' ? 'seal | SEALED' : 'open | OPEN');
    });
  }

  Future<void> _exportShare() async {
    final md = _exportMarkdown();
    try {
      await Share.share(md, subject: 'AZAI conversation');
    } catch (_) {
      await Clipboard.setData(ClipboardData(text: md));
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Export copied. Paste to share.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final locked = _runtime == 'SEALED';
    return Scaffold(
      appBar: AppBar(
        title: const Text('AZAI Remote'),
        actions: [
          IconButton(
            tooltip: 'Export / share',
            onPressed: _exportShare,
            icon: const Icon(Icons.ios_share),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text(
            'Jeeves Verified · Runtime $_runtime · Lamb $_lamb',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(color: kGold),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Text(limitation, style: Theme.of(context).textTheme.bodyMedium),
            ),
          ),
          const SizedBox(height: 18),
          TextField(
            controller: _prompt,
            enabled: !locked,
            decoration: const InputDecoration(
              labelText: 'Ask Jeeves',
              helperText: 'Companion only. Constitutional edits blocked. Text + export share.',
            ),
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 12,
            runSpacing: 8,
            children: [
              FilledButton(onPressed: locked ? null : _ask, child: const Text('Ask Jeeves')),
              OutlinedButton(
                onPressed: _seal,
                child: Text(locked ? 'Open Runtime' : 'Seal Runtime'),
              ),
              OutlinedButton(
                onPressed: _exportShare,
                child: const Text('Export / Share'),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text('Integrity', style: Theme.of(context).textTheme.titleSmall),
          const SizedBox(height: 8),
          Card(
            child: ListTile(
              title: Text('Peace $_lamb · Clarity $_lamb · Service $_lamb'),
              subtitle: const Text('Constitutional gate, not a proof of ethics.'),
            ),
          ),
          const SizedBox(height: 16),
          Text('Transcript', style: Theme.of(context).textTheme.titleSmall),
          ..._chat.map(
            (row) => Card(child: ListTile(title: Text(row))),
          ),
          const SizedBox(height: 16),
          Text('Receipts', style: Theme.of(context).textTheme.titleSmall),
          ..._receipts.take(8).map(
            (row) => Card(child: ListTile(title: Text(row))),
          ),
          const SizedBox(height: 24),
          Text(
            'Counted desktop download: https://azai-download-tracker.vibelock.workers.dev/',
            style: Theme.of(context).textTheme.bodySmall?.copyWith(color: kGoldDim),
          ),
        ],
      ),
    );
  }
}

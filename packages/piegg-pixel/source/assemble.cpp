// Repack the generated, green-backed motion strips into the Codex v2 grid.
#include <QCoreApplication>
#include <QDir>
#include <QFile>
#include <QImage>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QPainter>
#include <QRect>
#include <QStringList>
#include <algorithm>
#include <cmath>
#include <vector>

namespace {
constexpr int CellW = 192, CellH = 208;
struct Row { const char *name; int frames; };
const Row Rows[] = {{"idle", 6}, {"walking-right", 8}, {"walking-left", 8},
    {"waving", 4}, {"jumping", 5}, {"failed", 8}, {"waiting", 6},
    {"licking", 6}, {"review", 6}, {"gaze-0-7", 8}, {"gaze-8-15", 8}};

// Remove only the green screen; keep non-green colors and antialiased fur edges.
QImage removeGreen(const QImage &image) {
    const QImage src = image.convertToFormat(QImage::Format_ARGB32);
    QImage keyed(src.size(), QImage::Format_ARGB32);
    for (int y = 0; y < src.height(); ++y) {
        const auto *in = reinterpret_cast<const QRgb *>(src.constScanLine(y));
        auto *out = reinterpret_cast<QRgb *>(keyed.scanLine(y));
        for (int x = 0; x < src.width(); ++x) {
            const int r = qRed(in[x]), g = qGreen(in[x]), b = qBlue(in[x]);
            const int other = std::max(r, b), excess = g - other;
            const int alpha = excess <= 8 ? 255 : excess >= 55 ? 0 : (55 - excess) * 255 / 47;
            out[x] = alpha ? qRgba(r, std::min(g, other + 4), b, alpha) : qRgba(0, 0, 0, 0);
        }
    }
    return keyed;
}

struct Component { int id; int area; QRect box; };

// Find whole figures, rather than cutting through the slightly irregular slots
// produced by image generation. Small detached specks are ignored.
std::vector<Component> components(const QImage &image, std::vector<int> &labels) {
    const int w = image.width(), h = image.height();
    labels.assign(size_t(w) * h, 0);
    std::vector<Component> found;
    std::vector<int> queue;
    int nextId = 0;
    for (int y = 0; y < h; ++y) for (int x = 0; x < w; ++x) {
        const int start = y * w + x;
        if (labels[start] || qAlpha(image.pixel(x, y)) < 128) continue;
        const int id = ++nextId;
        int minX = x, minY = y, maxX = x, maxY = y;
        labels[start] = id; queue.clear(); queue.push_back(start);
        for (size_t cursor = 0; cursor < queue.size(); ++cursor) {
            const int current = queue[cursor], cx = current % w, cy = current / w;
            minX = std::min(minX, cx); maxX = std::max(maxX, cx);
            minY = std::min(minY, cy); maxY = std::max(maxY, cy);
            for (int dy = -1; dy <= 1; ++dy) for (int dx = -1; dx <= 1; ++dx) {
                const int nx = cx + dx, ny = cy + dy;
                if (nx < 0 || nx >= w || ny < 0 || ny >= h) continue;
                const int index = ny * w + nx;
                if (!labels[index] && qAlpha(image.pixel(nx, ny)) >= 128) {
                    labels[index] = id; queue.push_back(index);
                }
            }
        }
        if (queue.size() >= 500) found.push_back({id, int(queue.size()), QRect(QPoint(minX, minY), QPoint(maxX, maxY))});
    }
    return found;
}

QImage figure(const QImage &image, const std::vector<int> &labels, const Component &part, QRect &region) {
    region = part.box.adjusted(-3, -3, 3, 3).intersected(image.rect());
    QImage result(region.size(), QImage::Format_ARGB32);
    result.fill(Qt::transparent);
    const int w = image.width(), h = image.height();
    for (int y = region.top(); y <= region.bottom(); ++y) for (int x = region.left(); x <= region.right(); ++x) {
        const QRgb pixel = image.pixel(x, y);
        if (!qAlpha(pixel)) continue;
        bool keep = labels[y * w + x] == part.id;
        if (!keep && qAlpha(pixel) < 128) {
            for (int dy = -2; dy <= 2 && !keep; ++dy) for (int dx = -2; dx <= 2; ++dx) {
                const int nx = x + dx, ny = y + dy;
                if (nx >= 0 && nx < w && ny >= 0 && ny < h && labels[ny * w + nx] == part.id) { keep = true; break; }
            }
        }
        if (keep) result.setPixel(x - region.left(), y - region.top(), pixel);
    }
    return result;
}

double median(std::vector<double> values) {
    std::sort(values.begin(), values.end());
    const size_t mid = values.size() / 2;
    return values.size() % 2 ? values[mid] : (values[mid - 1] + values[mid]) / 2;
}
}

int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    if (argc != 3) {
        qWarning("Usage: piegg_sprite_assembler <package-dir> <preview-dir>");
        return 2;
    }
    const QDir package(QString::fromLocal8Bit(argv[1]));
    const QDir preview(QString::fromLocal8Bit(argv[2]));
    if (!QDir().mkpath(preview.path())) return 1;
    QImage atlas(CellW * 8, CellH * 11, QImage::Format_ARGB32_Premultiplied);
    atlas.fill(Qt::transparent);
    QJsonArray report;
    for (int rowIndex = 0; rowIndex < int(std::size(Rows)); ++rowIndex) {
        const Row row = Rows[rowIndex];
        const QImage strip(package.filePath(QString("source/rows/%1.png").arg(row.name)));
        if (strip.isNull()) { qWarning("Missing strip: %s", row.name); return 1; }
        const QImage keyed = removeGreen(strip);
        std::vector<int> labels;
        auto figures = components(keyed, labels);
        std::sort(figures.begin(), figures.end(), [](const Component &a, const Component &b) { return a.area > b.area; });
        if (figures.size() < size_t(row.frames)) {
            qWarning("Expected %d complete figures for %s, found %zu", row.frames, row.name, figures.size()); return 1;
        }
        figures.resize(row.frames);
        std::sort(figures.begin(), figures.end(), [](const Component &a, const Component &b) { return a.box.center().x() < b.box.center().x(); });
        std::vector<double> heights, bottoms;
        double maxWidth = 0;
        for (int i = 0; i < row.frames; ++i) {
            const QRect box = figures[i].box;
            heights.push_back(box.height());
            bottoms.push_back(box.bottom() + 1);
            maxWidth = std::max(maxWidth, double(box.width()));
        }
        const double scale = std::min(156.0 / median(heights), 164.0 / maxWidth);
        const double baseline = median(bottoms);
        QJsonArray frames;
        QDir().mkpath(preview.filePath(QString::fromLatin1(row.name)));
        for (int i = 0; i < row.frames; ++i) {
            const QRect box = figures[i].box;
            QRect region;
            const QImage cutout = figure(keyed, labels, figures[i], region);
            QImage cell(CellW, CellH, QImage::Format_ARGB32_Premultiplied);
            cell.fill(Qt::transparent);
            QPainter p(&cell);
            // Keep the deliberate pixel-art edges when fitting the sprite grid.
            p.setRenderHint(QPainter::SmoothPixmapTransform, false);
            const QRectF destination(96 - cutout.width() * scale / 2, 182 + (region.top() - baseline) * scale,
                                     cutout.width() * scale, cutout.height() * scale);
            p.drawImage(destination, cutout);
            p.end();
            QPainter painter(&atlas);
            painter.drawImage(QPoint(i * CellW, rowIndex * CellH), cell);
            painter.end();
            const QString output = preview.filePath(QString("%1/%2.png").arg(row.name).arg(i, 2, 10, QLatin1Char('0')));
            if (!cell.save(output)) return 1;
            const bool touchesEdge = box.left() <= 1 || box.right() >= strip.width() - 2 ||
                                     box.top() <= 1 || box.bottom() >= strip.height() - 2;
            frames.append(QJsonObject{{"frame", i}, {"width", box.width()}, {"height", box.height()},
                {"bottom", box.bottom() + 1}, {"touches_image_edge", touchesEdge}});
        }
        report.append(QJsonObject{{"row", rowIndex}, {"name", row.name}, {"scale", scale},
            {"baseline", baseline}, {"frames", frames}});
    }
    if (!atlas.save(package.filePath("spritesheet.png"))) return 1;
    QFile details(preview.filePath("assembly.json"));
    if (!details.open(QIODevice::WriteOnly)) return 1;
    details.write(QJsonDocument(QJsonObject{{"rows", report}}).toJson());
    QImage sheet(atlas.size(), QImage::Format_ARGB32_Premultiplied);
    sheet.fill(QColor("#f3f3f3"));
    QPainter p(&sheet);
    for (int y = 0; y < 11; ++y) for (int x = 0; x < 8; ++x)
        if ((x + y) % 2) p.fillRect(x * CellW, y * CellH, CellW, CellH, QColor("#e4e4e4"));
    p.drawImage(0, 0, atlas); p.end();
    if (!sheet.save(preview.filePath("contact-sheet.png"))) return 1;
    qInfo("Wrote %s and %s", qPrintable(package.filePath("spritesheet.png")), qPrintable(preview.filePath("assembly.json")));
    return 0;
}
